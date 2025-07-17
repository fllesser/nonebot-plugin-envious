import random
from random import choice
import re
from typing import Literal

from nonebot import get_driver, get_plugin_config, on_command, on_message, require
from nonebot.adapters.onebot.v11 import (
    GroupMessageEvent,
    Message,
    MessageEvent,
)
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Depends
from nonebot.plugin import PluginMetadata
from nonebot.typing import T_State

require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

from .config import Config
from .envious import GroupEnviousManager

__plugin_meta__ = PluginMetadata(
    name="羡慕 koishi",
    description="复读羡慕，并收纳关键词，自动羡慕",
    usage="羡慕xxx/清空羡慕/当前羡慕",
    type="application",
    config=Config,
    homepage="https://github.com/fllesser/nonebot-plugin-envious",
    supported_adapters={"~onebot.v11"},
)
econfig: Config = get_plugin_config(Config)
gem: GroupEnviousManager = GroupEnviousManager(econfig.envious_list)


@get_driver().on_startup
async def _():
    gem.load()
    logger.info(f"羡慕列表: {gem.envious_list}")
    logger.info(f"羡慕关键词最大长度: {MAX_LEN} 羡慕概率: {econfig.envious_probability}")


# 每天凌晨0点重置羡慕
@scheduler.scheduled_job(
    "cron",
    hour=0,
    minute=0,
    id="reset_envious",
    misfire_grace_time=60,
)
async def reset_envious():
    await gem.reset()
    logger.info("羡慕关键词已重置")


ENVIOUS_KEY: Literal["_envious_key"] = "_envious_key"
MAX_LEN: int = econfig.envious_max_len


def contains_keywords(event: MessageEvent, state: T_State) -> bool:
    if not isinstance(event, GroupMessageEvent):
        return False
    msg = event.get_message().extract_plain_text().strip()
    if not msg:
        return False
    if key := next((k for k in gem.envious_list if k in msg), None):
        if gem.triggered(event.group_id, key):
            return False
        state[ENVIOUS_KEY] = key
        return True
    return False


def Keyword() -> str:
    return Depends(_keyword)


def _keyword(state: T_State) -> str:
    return state[ENVIOUS_KEY]


# 自动羡慕
envious = on_message(rule=contains_keywords, priority=1027)


@envious.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, keyword: str = Keyword()):
    await gem.update_last_envious(event.group_id, keyword)
    await matcher.send("羡慕" + keyword)


# 复读羡慕，并收纳关键词
envious_cmd = on_command(cmd="羡慕", block=True)


@envious_cmd.handle()
async def _(matcher: Matcher, event: GroupMessageEvent, args: Message = CommandArg()):
    keyword = args.extract_plain_text().strip()
    gid = event.group_id

    if not keyword or "羡慕" in keyword or gem.triggered(gid, keyword):
        return
    if len(keyword) > MAX_LEN and (match := re.search(r"[0-9A-Za-z]+", keyword)):
        keyword = match.group(0)
    if len(keyword) > MAX_LEN:
        await matcher.finish("你在瞎羡慕什么呢？")
    # 概率不羡慕
    if random.random() > econfig.envious_probability:
        res = random.choice([f"怎么5202年了，还有人羡慕{keyword}啊", "不是, 这tm有啥好羡慕的"])
        await matcher.finish(res)

    await gem.update_last_envious(gid, keyword)
    gem.add_envious(keyword)
    await matcher.send("羡慕" + keyword)


@on_command(cmd="清空羡慕").handle()
async def _(matcher: Matcher):
    await gem.clear()
    await matcher.send("哼(`3´)，我啥也不会羡慕了")


ENVIOUS_MESSAGES = [
    "我现在超级羡慕{target}",
    "说实话，我真的好羡慕{target}",
    "唉，要是我也能像{target}就好了",
    "羡慕死了{target}",
    "现在最羡慕的就是{target}了",
]

NOT_ENVIOUS_MESSAGES = ["不好意思，我啥也不羡慕", "我对什么都很知足", "我现在很满足", "没有特别羡慕的呢"]


@on_command(cmd="当前羡慕").handle()
async def _(matcher: Matcher):
    if envious_list := gem.envious_list:
        target = "、".join(envious_list)
        res = choice(ENVIOUS_MESSAGES).format(target=target)
    else:
        res = choice(NOT_ENVIOUS_MESSAGES)
    await matcher.send(res)

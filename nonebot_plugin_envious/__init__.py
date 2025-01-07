import re
import json
import random
import asyncio

from pathlib import Path
from typing import Literal
from nonebot import (
    require,
    get_driver,
    get_plugin_config
)
from nonebot.log import logger
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.plugin import PluginMetadata
from nonebot.plugin.on import (
    on_command,
    on_message
)
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    MessageSegment,
    GroupMessageEvent
)
from .config import Config
from .envious import GroupEnviousManager


__plugin_meta__ = PluginMetadata(
    name="羡慕 koishi",
    description="复读羡慕，并收纳关键词，自动羡慕",
    usage="羡慕xxx/清空羡慕/当前羡慕",
    type="application",
    config=Config,
    homepage="https://github.com/fllesser/nonebot-plugin-envious",
    supported_adapters={ "~onebot.v11" }
)

ENVIOUS_KEY: Literal["_envious_key"] = "_envious_key"

econfig: Config = get_plugin_config(Config)
MAX_LEN: int = econfig.envious_max_len

gem: GroupEnviousManager = GroupEnviousManager(econfig.envious_list)

@get_driver().on_startup
async def _():
    gem.load()
    logger.info(f"羡慕列表: {gem.envious_list}")
    logger.info(f"羡慕关键词最大长度: {MAX_LEN} 羡慕概率: {econfig.envious_probability}")
    
    
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


envious = on_message(rule = contains_keywords, priority = 1027)
envious_cmd = on_command(cmd = '羡慕', block = True)
clear_envious = on_command(cmd = '清空羡慕')
list_envious = on_command(cmd = '当前羡慕')

@envious.handle()
async def _(event: GroupMessageEvent, state: T_State):
    keyword = state.get(ENVIOUS_KEY)
    await gem.update_last_envious(event.group_id, keyword)
    await envious.send("羡慕" + keyword)

@envious_cmd.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    keyword = args.extract_plain_text().strip()
    gid = event.group_id
    
    if not keyword or '羡慕' in keyword or gem.triggered(gid, keyword):
        return
    if len(keyword) > MAX_LEN and (match := re.search(r'[0-9A-Za-z]+', keyword)):
        keyword = match.group(0)
    if len(keyword) > MAX_LEN:
        await envious_cmd.finish("你在瞎羡慕什么呢？")
    # 概率不羡慕
    if random.random() > econfig.envious_probability:
        res = random.choice([
            f"怎么5202年了，还有人羡慕{keyword}啊",
            "不是, 这tm有啥好羡慕的"
        ])
        await envious_cmd.finish(res)
        
    await gem.update_last_envious(gid, keyword)
    gem.add_envious(keyword)
    await envious_cmd.send("羡慕" + keyword)

@clear_envious.handle()
async def _():
    await gem.clear()
    await clear_envious.send("哼(`3´)，我啥也不会羡慕了")
    
@list_envious.handle()
async def _():
    if envious_str := '、'.join(gem.envious_list):
        res = f"我现在巨tm羡慕{envious_str}"
    else:
        res = "不好意思，我啥也不羡慕"
    await list_envious.send(res)
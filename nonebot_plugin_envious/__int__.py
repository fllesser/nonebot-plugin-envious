import re
import json
import asyncio

from pathlib import Path
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

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

__plugin_meta__ = PluginMetadata(
    name="羡慕 koishi",
    description="复读羡慕，并收纳关键词，自动羡慕",
    usage="羡慕xxx/清空羡慕/当前羡慕",
    type="application",
    config=Config,
    homepage="https://github.com/fllesser/nonebot-plugin-envious",
    supported_adapters={ "~onebot.v11" }
)

ENVIOUS_KEY: str = "_envious_key"

econfig: Config = get_plugin_config(Config)
MAX_LEN: int = econfig.ENVIOUS_MAX_LEN
# 需要按字符串长度排序，换用 list
envious_list: list[str] = econfig.ENVIOUS_LIST
envious_file: Path = store.get_plugin_data_file("envious.json")

locks: dict[int, asyncio.Lock] = {}
last_envious: dict[int, str] = {}

@get_driver().on_startup
async def _():
    global envious_list, envious_file
    if not envious_file.exists():
        envious_file.write_text(json.dumps(envious_list))
    envious_list = json.loads(envious_file.read_text())
    logger.info(f"羡慕: {envious_list}")

def save_envious():
    global envious_list, envious_file
    envious_file.write_text(json.dumps(envious_list))

def contains_keywords(event: MessageEvent, state: T_State) -> bool:
    if not isinstance(event, GroupMessageEvent):
        return False
    msg = event.get_message().extract_plain_text().strip()
    if not msg:
        return False
    global envious_list
    if key := next((k for k in envious_list if k in msg), None):
        if key == last_envious.get(event.group_id):
            return False
        state[ENVIOUS_KEY] = key
        return True
    return False


envious = on_message(
    rule = contains_keywords,
    priority = 1027
)

add_keywords = on_command(
    cmd = '羡慕',
    block = True
)

clear_envious = on_command(
    cmd = '清空羡慕'
)

list_envious = on_command(
    cmd = '当前羡慕'
)

@envious.handle()
async def _(event: GroupMessageEvent, state: T_State):
    keyword = state.get(ENVIOUS_KEY)
    gid = event.group_id
    
    global locks, last_envious
    lock = locks.get(gid)
    if not lock:
        lock = asyncio.Lock()
        locks[gid] = lock
    async with lock:
        last_envious[gid] = keyword
        
    await envious.send("羡慕" + keyword)

@add_keywords.handle()
async def _(event: GroupMessageEvent, args: Message = CommandArg()):
    keyword = args.extract_plain_text().strip()
    gid = event.group_id
    
    global locks, last_envious
    if not keyword or '羡慕' in keyword or keyword == last_envious.get(gid):
        return
    if len(keyword) > MAX_LEN and (match := re.search(r'[0-9A-Za-z]+', keyword)):
        keyword = match.group(0)
    if len(keyword) > MAX_LEN:
        await add_keywords.finish("你在瞎羡慕什么呢？")
    
    lock = locks.get(gid)
    if not lock:
        lock = asyncio.Lock()
        locks[gid] = lock
    async with lock:
        last_envious[gid] = keyword
    if keyword not in envious_list:    
        envious_list.append(keyword)
        envious_list.sort(key=len, reverse=True)
        save_envious()
    await add_keywords.send("羡慕" + keyword)

@clear_envious.handle()
async def _():
    global envious_list, envious_file
    envious_list.clear()
    if envious_file.exists():
        envious_file.unlink()
    await clear_envious.send("哼(`3´)，我啥也不会羡慕了")
    
@list_envious.handle()
async def _():
    if envious_str := '、'.join(envious_list):
        res = f"我现在巨tm羡慕{envious_str}的人"
    else:
        res = "不好意思，我啥也不羡慕╭(╯^╰)╮"
    await list_envious.send(res)
import re
import json
import asyncio

from pathlib import Path
from nonebot import require, get_driver
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
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store

__plugin_meta__ = PluginMetadata(
    name="羡慕 koishi",
    description="羡慕 koishi",
    usage="羡慕",
    type="application",
    homepage="https://github.com/fllesser/nonebot-plugin-envious",
    supported_adapters={ "~onebot.v11" }
)


ENVIOUS_KEY: str = "_envious_key"
MAX_LEN: int = 8

keyword_set: set[str] = set()
locks: dict[int, asyncio.Lock] = {}
last_envious: dict[int, str] = {}

@get_driver().on_startup
async def _():
    keywords_file: Path = store.get_plugin_data_file("keywords.json")
    if not keywords_file.exists():
        keywords_file.write_text(json.dumps(["koishi"]))
    global keyword_set
    keyword_set = set(json.loads(keywords_file.read_text()))

def save_keywords():
    keywords_file: Path = store.get_plugin_data_file("keywords.json")
    keywords_file.write_text(json.dumps(list(keyword_set)))

def contains_keywords(event: MessageEvent, state: T_State) -> bool:
    if not isinstance(event, GroupMessageEvent):
        return False
    msg = event.get_message().extract_plain_text().strip()
    if not msg:
        return False
    if key := next((k for k in keyword_set if k in msg), None):
        if key == last_envious.get(event.group_id):
            return False
        state[ENVIOUS_KEY] = key
        return True
    return False


envious = on_message(
    rule = contains_keywords
)

add_keywords = on_command(
    cmd = '羡慕'
)

@envious.handle()
async def _(event: GroupMessageEvent, state: T_State):
    keyword = state.get(ENVIOUS_KEY)
    gid = event.group_id
    
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
    
    if not keyword or '羡慕' in keyword or keyword == last_envious.get(gid):
        return
    if len(keyword) > MAX_LEN and (match := re.search(r'[0-9A-Za-z]+', keyword)):
        keyword = match.group()
    if len(keyword) > MAX_LEN:
        return
    
    lock = locks.get(gid)
    if not lock:
        lock = asyncio.Lock()
        locks[gid] = lock
    async with lock:
        last_envious[gid] = keyword
        
    keyword_set.add(keyword)
    save_keywords()
    await add_keywords.send("羡慕" + keyword)
    
import json
import asyncio
from typing import Dict
from pathlib import Path
from nonebot import require

require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store


class LastEnvious:
    def __init__(self, last_envious: str):
        self.lock = asyncio.Lock()
        self.last_envious = last_envious
    
    def __eq__(self, other) -> bool:
        if isinstance(other, str):
            return self.last_envious == other
        return NotImplemented

    def __str__(self):
        return self.last_envious
        
    async def update(self, envious: str) -> None:
        async with self.lock:
            self.last_envious = envious


class GroupEnviousManager:
    def __init__(self, envious_list: list[str]):
        self.envious_list: list[str] = envious_list.copy()
        self.envious_file: Path = store.get_plugin_data_file("envious.json")
        self.group_envious: Dict[int, LastEnvious] = {}

    def load(self):
        if not self.envious_file.exists():
            self.save()
        self.envious_list = json.loads(self.envious_file.read_text())
    
    def save(self):
        self.envious_file.write_text(json.dumps(self.envious_list))

    def add_envious(self, envious: str):
        if envious not in self.envious_list:    
            self.envious_list.append(envious)
            self.envious_list.sort(key=len, reverse=True)
            self.save()
        
    async def update_last_envious(self, gid: int, envious: str):
        last_envious: LastEnvious = self.group_envious.get(gid)
        if last_envious:
            await last_envious.update(envious)
        else:
            self.group_envious[gid] = LastEnvious(envious)
            
    def triggered(self, gid: int, envious: str) -> bool:
        if last_envious := self.group_envious.get(gid):
            return last_envious == envious
        return False
        
    async def clear(self):
        self.envious_list.clear()
        if self.envious_file.exists():
            self.envious_file.unlink()
        for _, le in self.group_envious.items():
            await le.update("")
        
import asyncio
import json
from pathlib import Path

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
        # 默认羡慕列表
        self.default_envious_list: list[str] = envious_list.copy()
        # 当前羡慕列表
        self.envious_list: list[str] = envious_list.copy()
        # 羡慕记录文件
        self.envious_file: Path = store.get_plugin_data_file("envious.json")
        # 群的羡慕记录
        self.group_envious: dict[int, LastEnvious] = {}

    def load(self):
        """加载羡慕列表"""
        if not self.envious_file.exists():
            self.save()
        self.envious_list = json.loads(self.envious_file.read_text())

    def save(self):
        """保存羡慕列表"""
        self.envious_file.write_text(json.dumps(self.envious_list))

    def add_envious(self, envious: str):
        """添加羡慕词"""
        if envious not in self.envious_list:
            self.envious_list.append(envious)
            self.envious_list.sort(key=len, reverse=True)
            self.save()

    async def update_last_envious(self, gid: int, envious: str):
        """更新当前群的羡慕记录"""
        if last_envious := self.group_envious.get(gid):
            await last_envious.update(envious)
        else:
            self.group_envious[gid] = LastEnvious(last_envious=envious)

    def triggered(self, gid: int, envious: str) -> bool:
        """如果当前羡慕的词和上一次的相同，则返回 True"""
        return self.group_envious.get(gid) == envious

    async def reset(self):
        """重置羡慕列表，并清空所有群的羡慕记录"""
        self.envious_list = self.default_envious_list.copy()
        self.save()
        await asyncio.gather(*[le.update("") for le in self.group_envious.values()])

    async def clear(self):
        """清空所有群的羡慕记录"""
        self.envious_list.clear()
        self.save()
        await asyncio.gather(*[le.update("") for le in self.group_envious.values()])

<div align="center">
    <a href="https://v2.nonebot.dev/store">
    <img src="https://raw.githubusercontent.com/fllesser/nonebot-plugin-template/refs/heads/resource/.docs/NoneBotPlugin.svg" width="310" alt="logo"></a>

## ✨ nonebot-plugin-enviou ✨

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fllesser/nonebot-plugin-envious.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-envious">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-envious.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10|3.11|3.12|3.13-blue.svg" alt="python">
<a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v2.json" alt="ruff">
</a>
<a href="https://github.com/astral-sh/uv">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json" alt="uv">
</a>
</div>

</details>


## 📖 介绍

羡慕 koishi (`3´)

1. 群聊概率(默认0.7)复读羡慕
2. 触发羡慕会收纳关键词，可配置关键词的最大字数(默认10)，超过该值时，取其中的英文数字组合(超过最大字数忽略)
3. 为了防止刷屏，不会连续羡慕同一关键词

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-envious --upgrade
    
使用 pypi 源安装/更新

    nb plugin install nonebot-plugin-envious --upgrade -i https://pypi.org/simple
    
</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>conda</summary>

    uv add nonebot-plugin-envious
</details>
<details>
<summary>pip</summary>

    pip install nonebot-plugin-envious
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-envious
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-envious
</details>


打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_envious"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|       配置项        | 必填  |   默认值   |               说明                |
| :-----------------: | :---: | :--------: | :-------------------------------: |
|   envious_max_len   |  否   |     10     |  收纳羡慕关键词的最大字符串长度   |
| envious_probability |  否   |    0.7     | 羡慕概率，只可填 0 ~ 1.0 之间的值 |
|    envious_list     |  否   | ["koishi"] |           默认羡慕列表            |

## 🎉 使用
### 指令表
|   指令   | 权限  | 需要@ | 范围  |   说明   |
| :------: | :---: | :---: | :---: | :------: |
|   羡慕   | 群员  |  否   | 群聊  | 顾名思义 |
| 当前羡慕 | 群员  |  否   | 群聊  | 顾名思义 |
| 清空羡慕 | 群员  |  否   | 群聊  | 顾名思义 |

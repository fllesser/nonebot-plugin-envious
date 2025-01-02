<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-envious/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-envious/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-envious

_✨ 羡慕 Koishi ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/fllesser/nonebot-plugin-envious.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-envious">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-envious.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>

</details>


<details>
<summary>配置发布工作流</summary>

1. 前往 https://pypi.org/manage/account/#api-tokens 并创建一个新的 API 令牌。创建成功后不要关闭页面，不然你将无法再次查看此令牌。
2. 在单独的浏览器选项卡或窗口中，打开 [Actions secrets and variables](./settings/secrets/actions) 页面。你也可以在 Settings - Secrets and variables - Actions 中找到此页面。
3. 点击 New repository secret 按钮，创建一个名为 `PYPI_API_TOKEN` 的新令牌，并从第一步复制粘贴令牌。

</details>

## 📖 介绍

这里是插件的详细介绍部分

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-envious

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

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
<details>
<summary>conda</summary>

    conda install nonebot-plugin-envious
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_envious"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| 配置项1 | 是 | 无 | 配置说明 |
| 配置项2 | 否 | 无 | 配置说明 |

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 指令1 | 主人 | 否 | 私聊 | 指令说明 |
| 指令2 | 群员 | 是 | 群聊 | 指令说明 |

### 效果图
如果有效果图的话

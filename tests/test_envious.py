from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.log import logger
from nonebug import App
import pytest


def make_onebot_msg(message: Message) -> GroupMessageEvent:
    from time import time

    from nonebot.adapters.onebot.v11.event import Sender

    event = GroupMessageEvent(
        time=int(time()),
        sub_type="normal",
        self_id=123456,
        post_type="message",
        message_type="group",
        message_id=12345623,
        user_id=1234567890,
        group_id=1234567890,
        raw_message=message.extract_plain_text(),
        message=message,
        original_message=message,
        sender=Sender(),
        font=123456,
    )
    return event


@pytest.mark.asyncio
async def test_envious(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    from nonebot_plugin_envious import envious

    messages = [
        "koishi",
        "华为",
        "koishi",
        "koishi",
        "华为",
        "华为",
        "刘德华为什么很少演反派",
        "koishi",
        "刘德华为什么很少演反派",
    ]

    replys = [
        "羡慕 koishi",
        "羡慕华为",
        "羡慕 koishi",
        None,
        "羡慕华为",
        None,
        None,
        "羡慕 koishi",
        "羡慕华为",
    ]

    async with app.test_matcher(envious) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        for msg, reply in zip(messages, replys):
            logger.info(f"发送: {msg}, 期望回复: {reply}")
            event = make_onebot_msg(Message(msg))
            ctx.receive_event(bot, event)
            if reply:
                ctx.should_call_send(event, reply, result=None, bot=bot)
                logger.success(f"实际回复: {reply}")
            ctx.should_finished()

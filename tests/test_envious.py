from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.log import logger
from nonebug import App
import pytest


def make_onebot_msg(message: Message) -> GroupMessageEvent:
    from random import randint
    from time import time

    from nonebot.adapters.onebot.v11.event import Sender

    message_id = randint(1000000000, 9999999999)
    user_id = randint(1000000000, 9999999999)
    group_id = 123456789

    event = GroupMessageEvent(
        time=int(time()),
        sub_type="normal",
        self_id=123456,
        post_type="message",
        message_type="group",
        message_id=message_id,
        user_id=user_id,
        group_id=group_id,
        raw_message=message.extract_plain_text(),
        message=message,
        original_message=message,
        sender=Sender(user_id=user_id, nickname="TestUser"),
        font=123456,
    )
    return event


@pytest.mark.asyncio
async def test_envious(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    from nonebot_plugin_envious import envious, envious_cmd

    message_reply_tuples = [
        ("羡慕了", "羡慕了"),
        ("没事了", None),
        ("羡慕了", None),
        ("koishi", "羡慕 koishi"),
        ("没事了", None),
        ("华为", "羡慕华为"),
        ("koishi", "羡慕 koishi"),
        ("koishi", None),
        ("华为", "羡慕华为"),
        ("华为", None),
        ("刘德华为什么很少演反派", None),
        ("koishi", "羡慕 koishi"),
        ("刘德华为什么很少演反派", "羡慕华为"),
    ]

    async with app.test_matcher([envious_cmd, envious]) as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        for msg, reply in message_reply_tuples:
            logger.info(f"发送: {msg}, 期望回复: {reply}")
            event = make_onebot_msg(Message(msg))
            ctx.receive_event(bot, event)
            if reply:
                ctx.should_call_send(event, reply, result=None, bot=bot)
                logger.success(f"实际回复: {reply}")
            ctx.should_finished()

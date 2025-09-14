from typing_extensions import override

from fake import fake_group_message_event_v11, fake_private_message_event_v11
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment
from nonebot.log import logger
from nonebug import App
import pytest


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
            event = fake_group_message_event_v11(message=msg)
            ctx.receive_event(bot, event)
            if reply:
                ctx.should_call_send(event, reply, result=None, bot=bot)
                logger.success(f"实际回复: {reply}")
            ctx.should_finished()

        # 测试私聊
        event = fake_private_message_event_v11(message="koishi")
        ctx.receive_event(bot, event)
        ctx.should_finished()

        # 测试空文本消息
        message = Message(MessageSegment.image(file="https://www.baidu.com"))
        event = fake_group_message_event_v11(message=message)
        ctx.receive_event(bot, event)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_big_len_envious(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = fake_group_message_event_v11(
            message="羡慕青春的底色，要用“勇立潮头、勇争一流”的进取精神来绘。志不求易者成，事不避难者进。成功的道路绝不会是一马平川"
        )
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "不是, 你在瞎jb羡慕什么呢?", result=None, bot=bot)

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = fake_group_message_event_v11(
            message="羡慕青春的底色，要用“勇立潮头、勇争一流”的进取精神koishi来绘。志不求易者成，事不避难者进。成功的道路绝不会是一马平川"
        )
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "羡慕koishi", result=None, bot=bot)


@pytest.mark.asyncio
async def test_current_envious(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    from nonebot_plugin_envious import ENVIOUS_MESSAGES, NOT_ENVIOUS_MESSAGES, gem

    logger.info(f"TEST_CURRENT_ENVIOUS ||||||| envious_list: {gem.envious_list}")

    class CurrentEnviousResult:
        @override
        def __eq__(self, other) -> bool:
            assert isinstance(other, str)
            target = "、".join(gem.envious_list)

            for tem in ENVIOUS_MESSAGES:
                if tem.format(target=target) == other:
                    return True
            raise NotImplementedError

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = fake_group_message_event_v11(message="当前羡慕")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, CurrentEnviousResult(), result=None, bot=bot)  # type: ignore

    class NotEnviousResult:
        @override
        def __eq__(self, other) -> bool:
            assert isinstance(other, str)
            if other in NOT_ENVIOUS_MESSAGES:
                return True
            raise NotImplementedError

    await gem.clear()

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = fake_group_message_event_v11(message="当前羡慕")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, NotEnviousResult(), result=None, bot=bot)  # type: ignore


@pytest.mark.asyncio
async def test_envious_clear(app: App):
    import nonebot
    from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

    async with app.test_matcher() as ctx:
        adapter = nonebot.get_adapter(OnebotV11Adapter)
        bot = ctx.create_bot(base=Bot, adapter=adapter)
        event = fake_group_message_event_v11(message="清空羡慕")
        ctx.receive_event(bot, event)
        ctx.should_call_send(event, "啥也不羡慕了", result=None, bot=bot)

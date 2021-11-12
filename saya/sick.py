from graiax import silkcoder
from graia.application.message.parser.literature import Literature
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain

from tool.qqname import isaqqnum
from tool.yinluan import chs2yin
import random
from saya.TTS import t2s

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage],
                            inline_dispatchers=[Literature(".嘿嘿")]))
async def sick(
        app: GraiaMiraiApplication,
        group: Group,
        saying: MessageChain
):
    name = isaqqnum(saying.asDisplay())
    if not name:
        msg = chs2yin("{0}你怎么样，我最近过的不好{1}。".format(saying.asDisplay().strip(), "5" * random.randint(0, 10)))
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"" + msg * random.randint(1, 5))]
        ))
    else:
        msg = chs2yin("{0}你怎么样，我最近过的不好{1}。".format(name, "5" * random.randint(0, 10)))
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"" + msg * random.randint(1, 5))]
        ))



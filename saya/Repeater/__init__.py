from graia.saya import Saya, Channel
from graia.ariadne.model import Group
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.app import Ariadne

from saya import Including

import datetime
import threading


saya = Saya.current()
channel = Channel.current()

# Self-Including
readme = Including(author=None, group="角色功能", functions={
    "Repeater": {
        "describe": "复读",
        "show": False,
        "keys": []
        }
    }
)


counter = {}
limiter = {}

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def Repeater(app: Ariadne, group: Group, message: MessageChain):
    if message.asDisplay().startswith("["):
        pass
    else:
        if message.asDisplay() in counter.keys():
            counter[message.asDisplay()] += 1
        else:
            counter[message.asDisplay()] = 1
            try:
                limiter[message.asDisplay()] = limiter[message.asDisplay()] ** limiter[message.asDisplay()]
            except KeyError:
                limiter[message.asDisplay()] = 5
    try:
        if counter[message.asDisplay()] >= limiter[message.asDisplay()]:
            del counter[message.asDisplay()]
            await app.sendGroupMessage(group, message)
    except KeyError:
        pass

def clean():
    global counter
    counter = {}

    global limiter
    limiter = {}

    timer = threading.Timer(300, clean)
    timer.start()


timer = threading.Timer(300, clean)
timer.start()

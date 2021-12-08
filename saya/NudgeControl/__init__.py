from graia.broadcast.interrupt import InterruptControl
from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.mirai import NudgeEvent

from config.BFM_config import yaml_data
from saya import Including

# Self-Including
readme = Including(author=None, group="角色功能", functions={
            "Nudge": {
                "describe": "戳一戳",
                "show": True,
                "keys": [
                    "_戳一戳"
                ]
            }
        })


saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)


@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def send_back_nudge(app: GraiaMiraiApplication, nudge: NudgeEvent):
    if yaml_data["Basic"]["MAH"]["BotQQ"] == nudge.target:
        try:
            if nudge.context_type == "friend":
                await app.nudge(await app.getFriend(nudge.friend_id))
            elif nudge.context_type == "group":
                await app.nudge(await app.getMember(nudge.group_id, nudge.supplicant))
        except AttributeError:
            pass

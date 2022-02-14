from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.mirai import NewFriendRequestEvent

from saya import Including

# Self-Including
readme = Including(author=None, group="角色功能", functions={
            "DescribeYS": {
                "describe": "Unfinished",
                "show": False,
                "keys": [
                    "Unfinished"
                ]
            }
        })

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[NewFriendRequestEvent]))
async def get_bot_new_friend(events: NewFriendRequestEvent):
    await events.accept()

from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Member
from graia.ariadne.message.element import Plain, At

from config.BFM_config import yaml_data
from tool.mirai import restart
from tool.callcheck import wake_check
from saya import Including
from saya.ManagementControl import admins

import threading
import datetime

# Self-Including
readme = Including(author=None, group="防风控功能", functions={
            "ForceRestart": {
                "describe": "强制重启\n只",
                "show": True,
                "keys": [
                    "fre",
                    "force",
                    "restart"
                ]
            }
        })

saya = Saya.current()
channel = Channel.current()


def gettime():
    """
    get how long it should restart
    :return: how many second to next hour
    """
    now_time = datetime.datetime.now()

    next_time = now_time + datetime.timedelta(hours=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day

    next_time = datetime.datetime.strptime(
        str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 00:00:00",
        "%Y-%m-%d %H:%M:%S")

    timer_start_time = (next_time - now_time).total_seconds()
    return timer_start_time


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def reboot_handler(
        app: Ariadne,
        group: Group,
        member: Member,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["ForceRestart"]["keys"]):
        if member.id in admins():
            if restart():
                await app.sendGroupMessage(group, MessageChain.create([
                    At(member.id), Plain(f"如果您能看到这段话说明已经成功重启！")]
                ))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"抱歉！您没有执行此命令的权限！")]
            ))


timer = threading.Timer(gettime(), restart)
timer.start()

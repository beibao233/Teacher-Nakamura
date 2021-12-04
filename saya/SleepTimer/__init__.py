import ast
import time

from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain

from tool.callcheck import wake_check
from tool.qqname import isaqqnum
from saya import Including



# Self-Including
readme = Including(author=None, group="角色功能", functions={
            "sleep": {
                "describe": "开始晚安计时",
                "show": True,
                "keys": [
                    "_晚安",
                    "_睡了"
                ]
            },
            "wakeup": {
                "describe": "结束晚安计时",
                "show": True,
                "keys": [
                    "_早安",
                    "_早上好",
                    "_起了"
                ]
            }
        })

saya = Saya.current()
channel = Channel.current()

sleepList = {}

if sleepList == {}:
    with open("saya/SleepTimer/SleepList.cache", "r", encoding="utf-8") as _:
        sleepList = ast.literal_eval(_.read())


def write_cache(number, data):
    sleepList[number] = data
    with open("saya/CheckInControl/checkin.txt", "w+", encoding="utf-8") as _:
        _.write(str(sleepList))


def del_cache(number):
    del sleepList[number]
    with open("saya/CheckInControl/checkin.txt", "w+", encoding="utf-8") as _:
        _.write(str(sleepList))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def sleep_handler(
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["sleep"]["keys"]):
        if member.id in sleepList:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"你怎么还没去睡觉？{member.name}")]
            ))
        else:
            write_cache(number=member.id, data=time.time())
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"晚安{member.name}")]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def wakeup_handler(
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["sick"]["keys"]):
        if member.id in sleepList:
            sleep_time = time.strftime("%H小时%M分钟%S秒", time.localtime(time.time() - sleepList[member.id]))
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"醒了？{member.name}\n你睡了{sleep_time}")]
            ))
        else:
            write_cache(number=member.id, data=time.time())
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"{member.name}你没跟我说过你睡过觉啊？")]
            ))


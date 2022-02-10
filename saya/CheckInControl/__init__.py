from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

from tool.callcheck import wake_check
from saya import Including

import time
import yaml
import atexit

# Self-Including
readme = Including(author=None, group="基础功能", functions={
            "CheckIn": {
                "describe": "签到",
                "show": True,
                "keys": [
                    "ci",
                    "qd",
                    "签到"
                ]
            }
        })


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


checkinlist = {}
data = {}

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def CheckInFront(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["CheckIn"]["keys"]):
        if checkIn(member.id, member.name) == "in":
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"\n您今天在{getCheckinList()[member.id]['ltime']}的时候签到过了\n您已签到" + str(
                    getCheckinList()[member.id]['num']) + "次！")
            ]))
        else:
            output = getCheckinList()[member.id]['name'] + "\n签到成功!\n签到次数：" + str(
                getCheckinList()[member.id]['num']) + "\n签到时间：" + getCheckinList()[member.id][
                         'ltime']
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"" + output)
            ]))


def checkInAction(action, key, num):
    """
    Use to change data in check in list
    :param action: delete/add
    :param key: qq id
    :param num: how much you wanna change
    :return: changed checkinlist
    """
    data = {}
    if action == "delete":
        data["ltime"] = checkinlist[key]["ltime"]
        data['timestrip'] = checkinlist[key]['timestrip']
        data['num'] = checkinlist[key]['num'] - num
        data['name'] = checkinlist[key]['name']
        data['day'] = checkinlist[key]['day']
        checkinlist[key] = data
    elif action == "add":
        data["ltime"] = checkinlist[key]["ltime"]
        data['timestrip'] = checkinlist[key]['timestrip']
        data['num'] = checkinlist[key]['num'] + num
        data['name'] = checkinlist[key]['name']
        data['day'] = checkinlist[key]['day']
        checkinlist[key] = data
    return checkinlist


def checkIn(key, name):
    if key in checkinlist:
        if checkinlist[key]['day'] != time.strftime("%d", time.localtime(time.time())):
            data = {"ltime": time.strftime('%H:%M:%S', time.localtime(time.time())), 'timestrip': time.time(),
                    'num': checkinlist[key]['num'] + 1, 'name': name,
                    'day': time.strftime("%d", time.localtime(time.time()))}
            checkinlist[key] = data
            return checkinlist
        else:
            return "in"
    else:
        data = {}
        data["ltime"] = time.strftime('%H:%M:%S', time.localtime(time.time()))
        data['timestrip'] = time.time()
        data['num'] = 1
        data['name'] = name
        data['day'] = time.strftime("%d", time.localtime(time.time()))
        checkinlist[key] = data
        return checkinlist


def getMemberCheckData(qq):
    return checkinlist[qq]


def getCheckinList():
    return checkinlist


@atexit.register
def save_config():
    print(checkinlist)
    with open("config/config.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(checkinlist, f, allow_unicode=True, Dumper=NoAliasDumper)


if checkinlist == {}:
    with open("saya/CheckInControl/checkin.yaml", "r", encoding="utf-8") as f:
        file_data = f.read()
        checkinlist = yaml.load(file_data, Loader=yaml.FullLoader)

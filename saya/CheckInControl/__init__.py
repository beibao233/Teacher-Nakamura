from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member, Friend
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage, FriendMessage
from graia.application.message.elements.internal import Plain, MessageChain, At

from tool.callcheck import check
from config.BFM_config import yaml_data

import ast
import time
import ast
import random

checkinlist = {}
data = {}

saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def CheckInFront(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if check(message.asDisplay().strip(), [".checkin", ".签到", ".check", ".ci", ".qd"]):
        if checkIn(member.id, member.name) == "in":
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"您今天在{getCheckinList()[member.id]['ltime']}的时候签到过了\n您已签到" + str(
                    getCheckinList()[member.id]['num']) + "次！")
            ]))
        else:
            output = getCheckinList()[member.id]['name'] + "签到成功!\n签到次数：" + str(
                getCheckinList()[member.id]['num']) + "\n签到时间：" + getCheckinList()[member.id][
                         'ltime']
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"" + output)
            ]))


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def group_message_handler(
        app: GraiaMiraiApplication,
        friend: Friend,
        saying: MessageChain,
):
    if check(friend.id, yaml_data["Basic"]["Permission"]["Admin"]) and saying.startswith(".签增"):
        checkInAction("add", int(saying.asDisplay().split()[0]),
                      int(list(reversed(saying.asDisplay().split()))[0]))
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"成功！")
        ]))
    elif check(friend.id, yaml_data["Basic"]["Permission"]["Admin"]) and saying.startswith(".签减"):
        checkInAction("delete", int(saying.asDisplay().split()[0]),
                      int(list(reversed(saying.asDisplay().split()))[0]))
        await app.sendFriendMessage(friend, MessageChain.create([
            Plain(f"成功！")
        ]))


def checkInAction(action, key, num):
    data = {}
    if action == "delete":
        data["ltime"] = checkinlist[key]["ltime"]
        data['timestrip'] = checkinlist[key]['timestrip']
        data['num'] = checkinlist[key]['num'] - num
        data['name'] = checkinlist[key]['name']
        data['day'] = checkinlist[key]['day']
        checkinlist[key] = data
        with open("saya/CheckInControl/checkin.txt", "w+", encoding="utf-8") as f:
            f.write(str(checkinlist))
    elif action == "add":
        data["ltime"] = checkinlist[key]["ltime"]
        data['timestrip'] = checkinlist[key]['timestrip']
        data['num'] = checkinlist[key]['num'] + num
        data['name'] = checkinlist[key]['name']
        data['day'] = checkinlist[key]['day']
        checkinlist[key] = data
        with open("saya/CheckInControl/checkin.txt", "w+", encoding="utf-8") as f:
            f.write(str(checkinlist))
    return checkinlist


def checkIn(key, name):
    if key in checkinlist:
        if checkinlist[key]['day'] != time.strftime("%d", time.localtime(time.time())):
            data = {"ltime": time.strftime('%H:%M:%S', time.localtime(time.time())), 'timestrip': time.time(),
                    'num': checkinlist[key]['num'] + 1, 'name': name,
                    'day': time.strftime("%d", time.localtime(time.time()))}
            checkinlist[key] = data
            with open("saya/CheckInControl/checkin.txt", "w+", encoding="utf-8") as f:
                f.write(str(checkinlist))
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
        with open("saya/CheckInControl/checkin.txt", "w+", encoding="utf-8") as f:
            f.write(str(checkinlist))
        return checkinlist


def getMemberCheckData(qq):
    return checkinlist[qq]


def getCheckinList():
    return checkinlist


if checkinlist == {}:
    with open("saya/CheckInControl/checkin.txt", "r", encoding="utf-8") as f:
        checkinlist = ast.literal_eval(f.read())

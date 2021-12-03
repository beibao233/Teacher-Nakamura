import datetime
import threading
import ast
import httpx
import random

from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, At

from tool.callcheck import wake_check
from saya.CheckInControl import getCheckinList
from saya.CheckInControl import checkInAction


# Self-Including
class Including:
    def __init__(self):
        self.author = None
        self.group = "基础功能"
        self.functions = {
            "jrrp": {
                "describe": "今日人品",
                "show": True,
                "keys": [
                    "jrrp",
                    "今日人品",
                    "rp",
                    "嘉然日批"
                ]
            },
            "ntgm": {
                "describe": "逆天改命",
                "show": True,
                "keys": [
                    "ntgm",
                    "逆天改命",
                    "gm",
                ]
            },
            "EmperorList": {
                "describe": "欧皇榜",
                "show": True,
                "keys": [
                    "ohb",
                    "欧皇榜",
                ]
            },
            "ChieftainList": {
                "describe": "非酋榜",
                "show": True,
                "keys": [
                    "fqb",
                    "非酋榜",
                ]
            }
        }


saya = Saya.current()
channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrpIn(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), Including._functions["ntgm"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain(f"\n" + CdFl(member.id))]
        ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrpIn(app: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), _functions["jrrp"]["keys"]):
        if str(member.id) in getjrrplist():
            randint = getjrrplist()[str(member.id)]
            msg = "您今天的人品为：{0}".format(randint)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"\n" + msg)]
            ))
        else:
            randint = random.randint(0, 100)
            addjrrplist(str(member.id), randint)
            msg = "您今天的人品为：{0}".format(randint)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"\n" + msg)]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrpIn(app: GraiaMiraiApplication, group: Group, message: MessageChain):
    if wake_check(message.asDisplay(), _functions["EmperorList"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"欧皇榜：\n" + gentmsg4data(1) + "(仅显示前三)")]
        ))
    elif wake_check(message.asDisplay(), _functions["ChieftainList"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"非酋榜：\n" + gentmsg4data(0) + "(仅显示前三)")]
        ))


def turn2good_bad(qq):
    try:
        rp = getjrrplist()[str(qq)]
    except KeyError:
        return "在使用逆天改命前请先使用.jrrp"
    try:
        cin = getCheckinList()[qq]["num"]
    except KeyError:
        return "在使用逆天改命前请先使用.ci"
    if cin >= 3:
        if rp < 60:
            addjrrplist(str(qq), random.randint(0, 100))
            checkInAction("delete", qq, 3)
            return "您今天的人品为：{0}".format(getjrrplist()[str(qq)])
        else:
            return "您今天人品大于等于60\n无法逆天改命！"
    else:
        return "您的签到次数小于三\n无法逆天改命！"


def getjrrplist():
    """
    get charater data from cache
    (character data stand for 人品)
    :return: list with character data
    """
    return jrrplist


def getjrrpfromfile():
    """
    get character data from file
    (character data stand for 人品)
    :return: list with character data
    """
    with open("saya/DailyCharacterDataControl/jrrpdata.txt", "r", encoding='UTF-8') as f:
        jrrplist = ast.literal_eval(f.read())
    return jrrplist


jrrplist = getjrrpfromfile()


def gettime():
    """
    get how long it should clear data
    :return: how many second to next day
    """
    now_time = datetime.datetime.now()

    next_time = now_time + datetime.timedelta(days=+1)
    next_year = next_time.date().year
    next_month = next_time.date().month
    next_day = next_time.date().day

    next_time = datetime.datetime.strptime(
        str(next_year) + "-" + str(next_month) + "-" + str(next_day) + " 00:00:00",
        "%Y-%m-%d %H:%M:%S")

    timer_start_time = (next_time - now_time).total_seconds()
    return timer_start_time


def clearjrrplist():
    """
    when you call this function. It will delete the cache and save file data and restart timer
    :return: None
    """
    jrrplist.clear()
    with open("saya/DailyCharacterDataControl/jrrpdata.txt", "w+", encoding='UTF-8') as f:
        f.write("{}")
    timer = threading.Timer(gettime(), clearjrrplist)
    timer.start()


def addjrrplist(key, num):
    """
    add character data to file (character data stand for 人品)
    :param key: the user identification code (usually use the qq account number with str)
    :param num: the user character data to save (usually it's a number)
    :return: None
    """
    jrrplist[key] = num
    with open("saya/DailyCharacterDataControl/jrrpdata.txt", "w+") as f:
        f.write(str(jrrplist))


def gensortedjrrplist():
    """
    generate the sorted character data list (character data stand for 人品)
    :return: sorted jrrp list
    """
    jrrpList = getjrrpfromfile()
    sortedJrrpList = sorted(jrrpList.items(), key=lambda kv: (kv[1], kv[0]))
    return sortedJrrpList


def gentmsg4data(mode=0):
    """
    generate the character data list msg (character data stand for 人品)
    :param mode: 0 or 1
    :return: for mode 0 will return the worst character data list msg
             for mode 1 or other things will return the best character data list msg
    """
    msg = ""
    r = 0
    if mode == 0:
        for keys in gensortedjrrplist():
            if r < 3:
                msg = msg + "{}{name} 人品：{jrrp}\n"
                r += 1
                msg = msg.replace("{name}",
                                  ast.literal_eval(httpx.get("https://api.usuuu.com/qq/" + keys[0]).text)["data"][
                                      "name"]).replace("{jrrp}", str(getjrrpfromfile()[keys[0]]))
        return msg.format(str(1) + ".", str(2) + ".", str(3) + ".")
    elif mode != 0:
        for keys in reversed(gensortedjrrplist()):
            if r < 3:
                msg = msg + "{}{name} 人品：{jrrp}\n"
                r += 1
                msg = msg.replace("{name}",
                                  ast.literal_eval(httpx.get("https://api.usuuu.com/qq/" + keys[0]).text)["data"][
                                      "name"]).replace("{jrrp}", str(getjrrpfromfile()[keys[0]]))
        return msg.format(str(1) + ".", str(2) + ".", str(3) + ".")


timer = threading.Timer(gettime(), clearjrrplist)
timer.start()

import datetime
import threading
import ast
import random

import aiohttp
import yaml
import atexit

from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage, Friend, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At

from tool.callcheck import wake_check, wake_check_var
from saya.CheckInControl import getCheckinList
from saya.CheckInControl import checkInAction
from saya.ManagementControl import admins
from saya import Including

# Self-Including
readme = Including(author=None, group="人品功能", functions={
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
            },
            "PreAddJrrp": {
                "describe": "提前添加一个人的人品\nQQ号 人品",
                "show": False,
                "keys": [
                    "addjrrp",
                    "aj",
                ]
            },
        })


saya = Saya.current()
channel = Channel.current()

prejrrplist = {}

with open(f"{__file__.replace('__init__.py','')}jrrpdata.yaml", "r", encoding='UTF-8') as f:
    file_data = f.read()
    jrrplist = yaml.load(file_data, Loader=yaml.FullLoader)


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def prejrrpedhandler(app: Ariadne, friend: Friend, message: MessageChain):
    data = wake_check_var(message.asDisplay(), readme.functions["PreAddJrrp"]["keys"])
    if friend.id in admins() and data is not False:
        if len(data.split()) == 2:
            prejrrplist[data.split()[0]] = int(data.split()[1])
            timer4p = threading.Timer(gettime()+1, addplanedjrrp)
            timer4p.start()
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain("添加成功")]
            ))
        else:
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain("请检查语法")]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def ntgmhanlder(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["ntgm"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain(f"\n" + turn2good_bad(member.id))]
        ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrpIn(app: Ariadne, group: Group, message: MessageChain, member: Member):
    save_config()
    if wake_check(message.asDisplay().strip(), readme.functions["jrrp"]["keys"]):
        if str(member.id) in getjrrplist():
            randint = getjrrplist()[str(member.id)]
            msg = "您今天的人品为：{0}".format(randint)
            await app.sendGroupMessage(group, MessageChain.create([
                At(member.id), Plain(f"\n{msg}")]
            ))
        else:
            randint = random.randint(0, 100)
            addjrrplist(str(member.id), randint)
            msg = "您今天的人品为：{0}".format(randint)
            gy = ""
            if randint <= 60:
                async with aiohttp.ClientSession() as session:
                    async with session.get("https://v1.hitokoto.cn/?encode=text") as response:
                        gy += f"\n每日一言: {response.text}"
                        await app.sendGroupMessage(group, MessageChain.create([
                            At(member.id), Plain(f"\n{msg}{gy}")]
                        ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jrrp_list0all(app: Ariadne, group: Group, message: MessageChain):
    if wake_check(message.asDisplay(), readme.functions["EmperorList"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"欧皇榜：\n" + gentmsg4data(1) + "(仅显示前三)")]
        ))
    elif wake_check(message.asDisplay(), readme.functions["ChieftainList"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"非酋榜：\n" + gentmsg4data(0) + "(仅显示前三)")]
        ))


def addplanedjrrp():
    for _ in prejrrplist.keys():
        addjrrplist(_, prejrrplist[_])


def turn2good_bad(qq):
    save_config()
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
    with open(f"{__file__.replace('__init__.py','')}jrrpdata.yaml", "r", encoding='UTF-8') as f:
        file_data = f.read()
        jrrplist = yaml.load(file_data, Loader=yaml.FullLoader)
    return jrrplist


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


def gensortedjrrplist():
    """
    generate the sorted character data list (character data stand for 人品)
    :return: sorted jrrp list
    """
    jrrpList = getjrrplist()
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
    async with aiohttp.ClientSession() as session:
        if mode == 0:
            for keys in gensortedjrrplist():
                if r < 3:
                    msg = msg + "{}{name} 人品：{jrrp}\n"
                    r += 1
                    async with session.get(f"https://api.usuuu.com/qq/{keys[0]}") as response:
                        msg = msg.replace("{name}",
                                          ast.literal_eval(await response.text())
                                          ["data"]["name"]).replace("{jrrp}", str(getjrrplist()[keys[0]]))
                return msg.format(str(1) + ".", str(2) + ".", str(3) + ".")
        elif mode != 0:
            for keys in reversed(gensortedjrrplist()):
                if r < 3:
                    async with session.get(f"https://api.usuuu.com/qq/{keys[0]}") as response:
                        msg = msg + "{}{name} 人品：{jrrp}\n"
                        r += 1
                        msg = msg.replace("{name}",
                                          ast.literal_eval(await response.text())
                                          ["data"]["name"]).replace("{jrrp}", str(getjrrplist()[keys[0]]))
            return msg.format(str(1) + ".", str(2) + ".", str(3) + ".")


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


@atexit.register
def save_config():
    with open(f"{__file__.replace('__init__.py','')}jrrpdata.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(getjrrplist(), f, allow_unicode=True, Dumper=NoAliasDumper)


timer = threading.Timer(gettime(), clearjrrplist)
timer.start()

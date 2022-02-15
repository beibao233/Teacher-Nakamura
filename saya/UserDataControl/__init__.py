import datetime
import sqlite3

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import Friend, FriendMessage, Group, GroupMessage, Member
from graia.ariadne.event.mirai import NewFriendRequestEvent
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain
from graia.ariadne.model import BotMessage
from graia.broadcast.interrupt import InterruptControl
from graia.broadcast.interrupt.waiter import Waiter
from graia.saya import Saya, Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from config.BFM_config import yaml_data
from saya import Including
from tool.callcheck import wake_check_var
from tool.MemberDataBase import Member as DBMember, LoadMember, Message

# Self-Including
readme = Including(author=None, group="角色功能", functions={
            "DescribeYS": {
                "describe": "使用.reg ?获取更多帮助",
                "show": True,
                "keys": [
                    "reg",
                    "describe",
                    "注册",
                    "设置资料"
                ]
            }
        })

saya = Saya.current()
channel = Channel.current()
bcc = saya.broadcast
inc = InterruptControl(bcc)


def physical_gender_legit(gender: int):
    if gender in [0, 1, 2]:
        return gender
    else:
        return False


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_register(app: Ariadne, group: Group, saying: MessageChain):
    if wake_check_var(saying.asDisplay(), readme.functions["DescribeYS"]["keys"]) is not False:
        await app.sendGroupMessage(group, MessageChain.create([
            Plain(f"请添加{yaml_data['Basic']['BotName']}好友私聊问我吧！")]
        ))


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def user_register(app: Ariadne, friend: Friend, saying: MessageChain):

    @Waiter.create_using_function([FriendMessage])
    async def day_waiter(waiter_saying: MessageChain, waiter_friend: Friend):
        if int(waiter_saying.asDisplay()) in list(range(1, 31)) and waiter_friend.id == friend.id:
            return [True, int(waiter_saying.asDisplay())]

    @Waiter.create_using_function([FriendMessage])
    async def day2_waiter(waiter_saying: MessageChain, waiter_friend: Friend):
        if int(waiter_saying.asDisplay()) in list(range(1, 30)) and waiter_friend.id == friend.id:
            return [True, int(waiter_saying.asDisplay())]

    data = wake_check_var(saying.asDisplay(), readme.functions["DescribeYS"]["keys"])
    if data is not False:
        if data.strip() == "?" or "？":
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain(f""".reg 性别 生日月 生日天
                      性别: [0：女生 1：男生 2：隐藏]
                      生日月: 1-12
                      生日天: 1-31
                      使用数字代表性别仅为后台处理方便，并没有刻板化等意味。
                      如有异议，请联系此机器人主人QQ：{yaml_data['Basic']['Permission']['Master']}""")]
            ))
        if len(data.split()) == 3 and physical_gender_legit(int(data.split()[0])) is not False:
            try:
                user_birthday_date = datetime.datetime(1, int(data.split()[1]), int(data.split()[2]))
            except ValueError:
                try:
                    LoadMember(uid=friend.id)
                    await app.sendFriendMessage(friend, MessageChain.create([
                        Plain("日期有误，请重新单独发送生日天")]
                    ))
                    if int(data.split()[1]) == 2:
                        day_result = await inc.wait(day2_waiter)
                    else:
                        day_result = await inc.wait(day_waiter)
                    try:
                        if day_result[0]:
                            user_birthday_date = datetime.datetime(1, int(data.split()[1]), int(day_result[1]))
                        else:
                            await app.sendFriendMessage(friend, MessageChain.create([
                                Plain("输入失败！请检查日期合法性后重新进行注册！")]
                            ))
                    except ValueError:
                        await app.sendFriendMessage(friend, MessageChain.create([
                            Plain("输入失败！请检查日期合法性后重新进行注册！")]
                        ))
                except sqlite3.IntegrityError:
                    pass

            try:
                user_birthday = str(user_birthday_date.month) + str(user_birthday_date.day)
                DBMember(uid=friend.id, name=friend.nickname, gender=int(data.split()[0]), birthday=user_birthday)
                await app.sendFriendMessage(friend, MessageChain.create([
                    Plain(f"注册成功！{LoadMember(uid=friend.id).name}")]
                ))
            except sqlite3.IntegrityError:
                await app.sendFriendMessage(friend, MessageChain.create([
                    Plain(f"您已经注册过了！UID为: {LoadMember(uid=friend.id).uid}")]
                ))
            except NameError:
                pass

        elif not data.strip() == "?":
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain("请使用.reg ?获取帮助！")]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def group_message_saver(group: Group, member: Member, saying: MessageChain):
    Message(group.id, group.name, member.id, member.name, saying.asDisplay())


@channel.use(ListenerSchema(listening_events=[NewFriendRequestEvent]))
async def get_bot_new_friend(events: NewFriendRequestEvent):
    await events.accept()

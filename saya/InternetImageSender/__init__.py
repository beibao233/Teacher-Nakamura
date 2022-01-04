import httpx
import json
import yaml
import requests
import random
from saya import Including

from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Friend, Member, Group, FriendMessage, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, Image

from tool.callcheck import wake_check
from tool.qqname import isaqqnum

saya = Saya.current()
channel = Channel.current()

readme = Including(author=None, group="基础功能", functions={
    "xhl": {
        "describe": "随机小狐狸表情包",
        "show": True,
        "keys": [
            "xhl",
            "gxhl",
            "hl",
            "狐狸",
            "小狐狸"
        ]},
    "st": {
        "describe": "随机st",
        "show": False,
        "keys": [
            "st",
            "djj",
            "色图"
        ]}
})

with open('saya/InternetImageSender/member.yaml', 'r', encoding="utf-8") as f:
    file_data = f.read()
whitelist_data = yaml.load(file_data, Loader=yaml.FullLoader)


def get_sexphoto(qq):
    if qq in whitelist_data['MemberWhiteList']:
        with open("saya/InternetImageSender/cache.png", 'wb') as f:
            f.write(requests.get(
                json.loads(httpx.get("https://api.nyan.xyz/httpapi/sexphoto/").text)['data'][
                    'url'][0]).content)
        return True


def get_kemomimi(qq):
    if qq in whitelist_data['MemberBlackList']:
        with open("saya/InternetImageSender/cache.png", 'wb') as f:
            f.write(
                requests.get(
                    'https://brx86.gitee.io/kemomimi/{}.jpg'.replace("{}", str(random.randint(1, 581)))).content)
        return True


@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def st(
        app: GraiaMiraiApplication,
        friend: Friend,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["st"]["keys"]):
        data = get_sexphoto(friend.id)
        if data is True:
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain(f"\n北京市第三交通委提醒您：\n道路千万条\n安全第一条\n行车不规范\n亲人两行泪")]
            ))
            await app.sendFriendMessage(friend, MessageChain.create([
                Image.fromLocalFile("saya/InternetImageSender/cache.png").asFlash()
            ]))
        else:
            await app.sendFriendMessage(friend, MessageChain.create([
                Plain(f"您没有权限，抱歉！" )]
            ))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def xhl(
        app: GraiaMiraiApplication,
        group: Group,
        member: Member,
        saying: MessageChain
):
    if wake_check(saying.asDisplay(), readme.functions["xhl"]["keys"]):
        data = get_kemomimi(member.id)
        if data is True:
            await app.sendGroupMessage(group, MessageChain.create([
                Image.fromLocalFile("saya/InternetImageSender/cache.png")
            ]))
        else:
            await app.sendGroupMessage(group, MessageChain.create([
                Plain(f"您没有权限，抱歉！")]
            ))

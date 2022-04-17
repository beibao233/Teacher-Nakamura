from graia.saya import Saya, Channel
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage, Member
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Plain, Voice, Image

from tool.callcheck import wake_check
from saya import Including
from graiax import silkcoder
from PIL import Image as Images

import io

# 瞎写（
# Self-Including
readme = Including(author=None, group="网络游戏", functions={
            "XiaoBaWang": {
                "describe": "小霸王",
                "show": True,
                "keys": [
                    "_小霸王",
                ]},
            "LifeRestart": {
                "describe": "人生重开",
                "show": True,
                "keys": [
                    "_人生重开",
                ]},
            "JJZ": {
                "describe": "绝绝子",
                "show": True,
                "keys": [
                    "_绝绝子",
                ]},
            "FSSML": {
                "describe": "发生什么事了",
                "show": True,
                "keys": [
                    "_发生什么事了",
                ]}
        })


saya = Saya.current()
channel = Channel.current()


def image_to_byte_array(image: Images):
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def xbw(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["XiaoBaWang"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("https://www.yikm.net/")]))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def lr(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["LifeRestart"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([At(member.id),
                                                               Plain("http://liferestart.syaro.io/public/index.html")]))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def jjz(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["JJZ"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([At(member.id), Plain("https://kingcos.me/jjz/")]))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def fssmsl(app: Ariadne, group: Group, message: MessageChain, member: Member):
    if wake_check(message.asDisplay().strip(), readme.functions["FSSML"]["keys"]):
        await app.sendGroupMessage(group, MessageChain.create([
            At(member.id), Plain("发生什么事了🔈" * 10),
            Image(data_bytes=image_to_byte_array(Images.open('saya/MessageInCodeSender/Image/发生什么事了.png')))
                                                               ]))

        await app.sendGroupMessage(group, MessageChain.create([
            Voice(data_bytes=await silkcoder.async_encode('saya/MessageInCodeSender/Voice/发生什么事了.mp3'))
        ]))

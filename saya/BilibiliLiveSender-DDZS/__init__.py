from graia.saya import Saya, Channel
from graia.ariadne.model import Member
from graia.ariadne.app import Ariadne
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.event.message import Group, GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Plain, At
from graia.ariadne.event.lifecycle import ApplicationLaunched
from graia.scheduler.saya import SchedulerSchema
from graia.scheduler import timers
from graia.ariadne.exception import UnknownTarget

from tool.MemberDataBase import GroupBilibiliSub, LoadBilibiliSub
from tool.callcheck import wake_check_var
from saya import Including

import loguru
import json
import aiohttp

# Self-Including
readme = Including(author=None, group="B站功能", functions={
    "SubOneByUid": {
        "describe": "在群内关注UP主",
        "show": True,
        "keys": [
            "关注",
            "sub"
        ]
    }
})

saya = Saya.current()
channel = Channel.current()

currentLive = []
sentLive = []


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def SubOneByUid(app: Ariadne, group: Group, message: MessageChain, member: Member):
    result = wake_check_var(message.asDisplay(), readme.functions["SubOneByUid"]["keys"])

    if result is not False:
        result = result.strip()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.bilibili.com/x/space/acc/info?mid={result}") as response:
                if result is not False and json.loads(await response.text())["code"] != -400:
                    GroupBilibiliSub(group.id, json.loads(await response.text())
                    ["data"]["live_room"]["roomid"], member.id)
                    await app.sendGroupMessage(group, MessageChain.create([
                        At(member.id), Plain(f"关注{json.loads(await response.text())['data']['name']}成功！"
                                             f"\n将在开始直播的时候在本群通知您！")
                    ]))


@channel.use(ListenerSchema(listening_events=[ApplicationLaunched]))
@channel.use(SchedulerSchema(timer=timers.every_custom_minutes(5)))
async def CheckAndSendLiveOnMessage(app: Ariadne):
    loguru.logger.info("检查数据库中直播间并将正直播加入正直播列表！")

    if LoadBilibiliSub().sublist != {}:
        for SubData in LoadBilibiliSub().sublist:
            async with aiohttp.ClientSession() as session:
                for SingleSubData in LoadBilibiliSub().sublist[SubData]:
                    async with session.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom"
                                           f"?room_id={SingleSubData[0]}"
                                           ) as response:
                        try:
                            if json.loads(await response.text())["data"]["room_info"]["live_status"] == 1:
                                if not SubData[0] in currentLive:
                                    currentLive.append({SubData: SingleSubData})
                            else:
                                currentLive.remove({SubData: SingleSubData})
                                sentLive.remove({SubData: SingleSubData})
                        except ValueError:
                            pass
                        except TypeError:
                            pass

    loguru.logger.info("检查正直播列表并发送")
    for LiveCurrentOn in currentLive:
        if LiveCurrentOn not in sentLive:
            sentLive.append(LiveCurrentOn)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.live.bilibili.com/xlive/web-room/v1/index/getInfoByRoom?room_id="
                                       f"{LiveCurrentOn[list(LiveCurrentOn.keys())[0]][0]}",
                                       ) as response:
                    async with session.get(f"https://api.bilibili.com/x/space/acc/info?mid="
                                           f"{json.loads(await response.text())['data']['room_info']['uid']}") as \
                            U_response:
                        ApiResponse = json.loads(await response.text())
                        U_ApiResponse = json.loads(await U_response.text())
                        MessageOfLive = \
                            f"UP主:{U_ApiResponse['data']['name']}\n" \
                            f"直播标题:{ApiResponse['data']['room_info']['title']}\n" \
                            f"直播链接:https://live.bilibili.com/{ApiResponse['data']['room_info']['room_id']}"
            await app.sendGroupMessage(int(list(LiveCurrentOn.keys())[0].replace("_", "")),
                                       MessageChain.create(Plain(MessageOfLive)))
            try:
                await app.sendFriendMessage(LiveCurrentOn[list(LiveCurrentOn.keys())[0]][1],
                                           MessageChain.create(Plain(MessageOfLive)))
            except UnknownTarget:
                pass

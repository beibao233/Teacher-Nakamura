from graia.saya import Saya
from graia.ariadne.app import Ariadne
from graia.broadcast import Broadcast
from graia.scheduler import GraiaScheduler
from graia.ariadne.model import MiraiSession
from graia.broadcast.interrupt import InterruptControl
from graia.scheduler.saya import GraiaSchedulerBehaviour
from graia.saya.builtins.broadcast import BroadcastBehaviour

from graia.ariadne.entry import AccountNotFound

from loguru import logger

from config.BFM_config import yaml_data, save_config
from tool import mirai

import os
import asyncio


loop = asyncio.get_event_loop()
bcc = Broadcast(loop=loop)
scheduler = GraiaScheduler(loop, bcc)
inc = InterruptControl(bcc)

saya = Saya(bcc)
saya.install_behaviours(BroadcastBehaviour(bcc))
saya.install_behaviours(GraiaSchedulerBehaviour(scheduler))
saya.install_behaviours(InterruptControl(bcc))

mirai.start()

app = Ariadne(
    broadcast=bcc,
    connect_info=MiraiSession(
        host=yaml_data['Basic']['MAH']['MiraiHost'],
        verify_key=yaml_data['Basic']['MAH']['VerifyKey'],
        account=yaml_data['Basic']['MAH']['BotQQ']
    )
)

with saya.module_context():
    os.chdir(os.path.abspath(os.path.dirname(__file__)))
    for module in os.listdir("saya"):
        if module == "__pycache__":
            continue
        if os.path.isdir(module):
            saya.require(f"saya.{module}")
        else:
            saya.require(f"saya.{module.split('.')[0]}")
    logger.info("加载成功！")



try:
    app.launch_blocking()
except KeyboardInterrupt:
    save_config()
except AccountNotFound:
    save_config()
    print("未能使用所配置的账号激活 sessionKey, 请检查 config.yaml 配置是否正确或检查 mirai 是否正常登录该账号")




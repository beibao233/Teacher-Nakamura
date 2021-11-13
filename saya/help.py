from graia.saya import Saya, Channel
from graia.application import GraiaMiraiApplication, Member
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.application.event.messages import Group, GroupMessage
from graia.application.message.elements.internal import Plain, MessageChain, At

from config.BFM_config import yaml_data
from tool.callcheck import check
from saya.CheckInControl import getCheckinList
from saya.CheckInControl import checkInAction


saya = Saya.current()
channel = Channel.current()


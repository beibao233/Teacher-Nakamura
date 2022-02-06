import atexit
import os
import subprocess
from subprocess import DEVNULL
from config.BFM_config import yaml_data


def start():
    try:
        path = os.path.abspath(os.path.dirname(__file__)).replace("\\tool", "") + "/" + yaml_data['Basic'][
            'MiraiPath']
        os.chdir(path)
        global mirai
        mirai = subprocess.Popen(path + "java/bin/java.exe -jar " + path + "/" + "mcl.jar", stdout=DEVNULL)
        return True
    except:
        return False


def restart():
    """
    Way to restart Mirai Console
    :return: True
    """
    if halt():
        if start():
            return True


@atexit.register
def halt():
    try:
        os.system('taskkill.exe /f /pid:' + str(mirai.pid))
        return True
    except:
        return False



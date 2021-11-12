import atexit
import os
import subprocess
from subprocess import DEVNULL
from config.BFM_config import yaml_data


def start():
    path = os.path.abspath(os.path.dirname(__file__)).replace("\\tool", "") + "/" + yaml_data['Basic'][
        'MiraiPath']
    os.chdir(path)
    mirai = subprocess.Popen(path + "java/bin/java.exe -jar " + path + "/" + "mcl.jar", stdout=DEVNULL)

    @atexit.register
    def clean():
        os.system('taskkill.exe /f /pid:' + str(mirai.pid))




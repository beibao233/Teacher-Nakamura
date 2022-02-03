import os
import yaml
import atexit

from pathlib import Path

global yaml_data


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


if not os.path.exists('config/config.yaml'):
    print('未检测到配置文件！')
    exit()
else:
    with open('config/config.yaml', 'r', encoding="utf-8") as f:
        file_data = f.read()
    yaml_data = yaml.load(file_data, Loader=yaml.FullLoader)

MIRAI_PATH = Path(yaml_data["Basic"]["MiraiPath"])
CONFIG_PATH = MIRAI_PATH.joinpath("config", "net.mamoe.mirai-api-http")
if not CONFIG_PATH.exists():
    print(f"请修改配置文件中的 Basic-MiraiPath 为Mirai的根目录")
    exit()


@atexit.register
def save_config(data=yaml_data):
    with open("config/config.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, Dumper=NoAliasDumper)


save_config()

import os
import yaml

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
VIOCE_PATH = MIRAI_PATH.joinpath("data", "net.mamoe.mirai-api-http", "voices")
if not VIOCE_PATH.exists():
    print(f"请修改配置文件中的 Basic-MiraiPath 为Mirai的根目录")
    exit()


def save_config():
    print("正在保存配置文件")
    with open("config/config.yaml", 'w', encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, Dumper=NoAliasDumper)


save_config()

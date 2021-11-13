<div align="center"><img src="https://z3.ax1x.com/2021/11/13/IrhHRH.png" alt="Icon" title="Icon" /><br><center style="color:gray">名字来自于《日常》里的中村加奈</center></div>

# Teacher-Nakamura 中村老师

### 为什么选用中村老师做机器人？

1. > 屠龙者终成恶龙

2. 可以将原未公开的背讯功能性机器人无缝衔接起来

### 上游用了什么？

1.[Mirai](!https://github.com/mamoe/mirai)

2.[Mirai-Http-API](!https://github.com/project-mirai/mirai-api-http)

3.[Graia-Framework](!https://github.com/GraiaProject/Application)

### 开发状态？

> 正在从老版本移植功能，在主要功能移植完毕后。会主要开发角色模拟方面的功能
>
> （例如图灵机器人 青云客和腾讯闲聊的API）

### 如何部署？

> 0.确保您的Python版本为3.8（其他版本未经测试可能有出现问题）
>
> 	使用pip install -r requirements.txt安装需求库

1.本项目支持自动带起<a href="https://github.com/iTXTech/mirai-console-loader">Mirai Console Loader</a>，使用<a href="https://github.com/iTXTech/mcl-installer">iTXTech MCL Installer</a>在您设定的Mirai根目录下安装MCL（默认路径为 /mirai ）

2.安装完成后请将该目录下的 config.json 替换为下列内容 

```json
{
  "js_optimization_level": -1,
  "mirai_repo": "https://gitee.com/peratx/mirai-repo/raw/master",
  "maven_repo": [
    "https://maven.aliyun.com/repository/public"
  ],
  "packages": [
    {
      "id": "net.mamoe:mirai-console",
      "channel": "beta",
      "version": "2.7.1",
      "type": "libs",
      "versionLocked": true
    },
    {
      "id": "net.mamoe:mirai-console-terminal",
      "channel": "beta",
      "version": "2.7.1",
      "type": "libs",
      "versionLocked": true
    },
    {
      "id": "net.mamoe:mirai-core-all",
      "channel": "beta",
      "version": "2.7.1",
      "type": "libs",
      "versionLocked": true
    },
    {
      "id": "org.itxtech:mcl-addon",
      "channel": "c122",
      "version": "1.2.2",
      "type": "plugins",
      "versionLocked": false
    }
  ],
  "disabled_scripts": [],
  "proxy": "",
  "log_level": 1,
  "script_props": {}
}
```

3. 下载<a href="https://github.com/project-mirai/mirai-api-http/releases/tag/v1.12.0">Mirai-Http-API</a> 1.X版本。下载jar文件后将文件放在该目录下的plugins文件夹下，启动MCL。等待Console出现类似的提示信息后记录auth Key和server IP。

   [![IsJQdf.md.png](https://z3.ax1x.com/2021/11/13/IsJQdf.md.png)](https://imgtu.com/i/IsJQdf)

   使用如下的指令在MCL中设置你您的机器人登录

   ```
   /autoLogin add 机器人QQ号 QQ密码
   ```

   <font color=red>__请注意！ 必须使用/stop才能保存自动登录设定！__</font>

4. 打开项目根目录下的 config 文件夹下的 config.yaml

   ```yaml
   Basic:
     BotName: 默认名字-请更改
     MAH:
       BotQQ: 数字-机器人QQ号
       MiraiAuthKey: 字符串-MAH登录密钥
       MiraiHost: http://localhost:8080
     MiraiPath: mirai/
     Permission:
       Admin:
       - 管理员QQ
       Master: 主人QQ
       MasterName: 主人名字
   Saya:
   ```

	把刚刚从Console里获取到的auth Key填进去， 更改机器人的QQ号。其他自定义就可以。

5.双击start.bat启动

6.Have fun :D

### 感谢

Mirai和Graia等库的开发让这个项目可能

<a href="https://github.com/djkcyl">A60</a> 感谢解答部分环境配置问题

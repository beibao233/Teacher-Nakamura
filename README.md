<div align="center"><img src="https://z3.ax1x.com/2021/11/13/IrhHRH.png" alt="Icon" title="Icon" /><br><center style="color:gray">名字来自于《日常》里的中村加奈</center></div>

# Teacher-Nakamura 中村老师

### 为什么选用中村老师做机器人？

1. > 屠龙者终成恶龙

2. 可以将原未公开的背讯功能性机器人无缝衔接起来

### 上游用了什么？

1.<a href="https://github.com/mamoe/mirai">Mirai</a>

2.<a href="https://github.com/project-mirai/mirai-api-http">Mirai-Http-API</a>

3.<a href=https://github.com/GraiaProject/Ariadne>Ariadne</a>

### 开发状态？

> 正在从老版本移植功能，在主要功能移植完毕后。会主要开发角色模拟方面的功能
>
> （例如图灵机器人 青云客和腾讯闲聊的API）

### 如何部署？

0. 确保您的Python版本为3.9.10（其他版本未经测试可能有出现问题）
   使用pip install -r requirements.txt安装需求库

1. 本项目支持自动带起<a href="https://github.com/iTXTech/mirai-console-loader">Mirai Console Loader</a>，使用<a href="https://github.com/iTXTech/mcl-installer">iTXTech MCL Installer</a>在您设定的Mirai根目录下安装MCL（默认路径为 /mirai ）

2. 在启动Mirai Console Loader后下载<a href="https://github.com/project-mirai/mirai-api-http">Mirai-Http-API</a>最新版
   放在MCL安装目录下的plugins文件中
   
3. 使用如下的指令在MCL中设置你您的机器人登录

   ```
   /autoLogin add 机器人QQ号 QQ密码
   ```

   <font color=red>__请注意！ 必须使用/stop才能保存自动登录设定！__</font>

4. 在MCL的安装目录下找到settings.yaml
   （在/config/net.mamoe.mirai-api-http/setting.yml）
   修改文件成
   ```yaml
    adapters:
      - http
      - ws
    debug: false
    enableVerify: true
    verifyKey: ServiceVerifyKey # 你可以自己设定, 这里作为示范
    singleMode: false
    cacheSize: 4096 # 可选, 缓存大小, 默认4096. 缓存过小会导致引用回复与撤回消息失败
    adapterSettings:
      ## 详情看 http adapter 使用说明 配置
      http:
        host: localhost
        port: 8080 # 端口
        cors: [*]
    
      ## 详情看 websocket adapter 使用说明 配置
      ws:
        host: localhost
        port: 8080 # 端口
        reservedSyncId: -1
        ## 确保为 -1, 否则 WebsocketAdapter(Experimental) 没法正常工作.
    ```

5. 打开项目根目录下的 config 文件夹下的 config.yaml

   ```yaml
   Basic:
     BotName: 默认名字-请更改
     MAH:
       BotQQ: 数字-机器人QQ号
       VerifyKey: 字符串-MAH登录密钥
       MiraiHost: http://localhost:8080
     MiraiPath: mirai/
     Permission:
       Admin:
       - 管理员QQ
       Master: 主人QQ
       MasterName: 主人名字
     WakeText: .
   Saya:
   ```

	把刚刚在setttings.yaml文件里的到的verifyKey填进去， 更改机器人的QQ号。其他自定义就可以。

6.直接启动main.py

7.Have fun :D

### 感谢

Mirai和Ariadne等库的开发让这个项目可能

<a href="https://github.com/djkcyl">A60</a> 感谢解答部分环境配置问题

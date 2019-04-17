# wsmud-game
武神传说日常脚本
---
运行需要安装websocket-client





配置说明:



```
pip install websocket-client

python demo.py [username] [password] [zone]

```

脚本说明:

    运行流程

    1:登陆判断是否完成师门

    2:未完成,去买20个包子

    3:回到师门,刷到包子任务提交

    4:完成师门之后,刷副本, 副本为进入直接退出 ,需要修改的话,修改 wsgame.py中fuben以及richang函数

    5:每次刷完副本都会判断是否完成每日签到,完成则挖矿,否则继续副本

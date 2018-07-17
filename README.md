# wsmud-game
武神传说日常脚本
---
主要修改 demo.py中的main 部分 创建thread的参数
参数1
![参数1](https://i.loli.net/2018/07/17/5b4d5b9a05b18.png)

参数2 3
![参数2 3](https://i.loli.net/2018/07/17/5b4d5b9a2469c.png)

参数4 为 师父的名字,

另外,每个师父的所在位置不同,所以找到师父位置的函数也需要进行修改

逍遥的例子如下:
```
    def sm(self,ws):
        ws.send("jh fam 5 start")
        time.sleep(1)
        print(self.smflag)
        while self.smflag:
            time.sleep(1)
            ws.send("task sm "+self.smid)
```

# edit by knva
# tool VSCODE
# time 2018-8-2 10:12:27
import threading
import websocket

from wsgamePlayer import wsgamePlayer

try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import re


def sendcmd(ws, cmd):
    cmd = cmd.split(";")
    for i in cmd:
        ws.send(i)


class wsgame:
    smflag = True
    yjdid = ''
    smid = ''
    rc = False
    sfname = "苏星河"
    mp = ''
    dxerid = ''
    dxename = "店小二"
    baoziid = ''
    serverip = ''
    acctoken = ''
    palyer = ''
    smcode = 1
    die = False
    myname = ''
    zbid = ''
    addr = {"住房": "jh fam 0 start;go west;go west;go north;go enter",
            "住房-卧室": "jh fam 0 start;go west;go west;go north;go enter;go north",
            "住房-小花园": "jh fam 0 start;go west;go west;go north;go enter;go northeast",
            "住房-炼药房": "jh fam 0 start;go west;go west;go north;go enter;go southwest",
            "住房-练功房": "jh fam 0 start;go west;go west;go north;go enter;go west",
            "扬州城-钱庄": "jh fam 0 start;go north;go west;store",
            "扬州城-广场": "jh fam 0 start",
            "扬州城-醉仙楼": "jh fam 0 start;go north;go north;go east",
            "扬州城-杂货铺": "jh fam 0 start;go east;go south",
            "扬州城-打铁铺": "jh fam 0 start;go east;go east;go south",
            "扬州城-药铺": "jh fam 0 start;go east;go east;go north",
            "扬州城-衙门正厅": "jh fam 0 start;go west;go north;go north",
            "扬州城-镖局正厅": "jh fam 0 start;go west;go west;go south;go south",
            "扬州城-矿山": "jh fam 0 start;go west;go west;go west;go west",
            "扬州城-喜宴": "jh fam 0 start;go north;go north;go east;go up",
            "扬州城-擂台": "jh fam 0 start;go west;go south",
            "扬州城-当铺": "jh fam 0 start;go south;go east",
            "扬州城-帮派": "jh fam 0 start;go south;go south;go east",
            "帮会-大门": "jh fam 0 start;go south;go south;go east;go east",
            "帮会-大院": "jh fam 0 start;go south;go south;go east;go east;go east",
            "帮会-练功房": "jh fam 0 start;go south;go south;go east;go east;go east;go north",
            "帮会-聚义堂": "jh fam 0 start;go south;go south;go east;go east;go east;go east",
            "帮会-仓库": "jh fam 0 start;go south;go south;go east;go east;go east;go east;go north",
            "帮会-炼药房": "jh fam 0 start;go south;go south;go east;go east;go east;go south",
            "扬州城-扬州武馆": "jh fam 0 start;go south;go south;go west",
            "扬州城-武庙": "jh fam 0 start;go north;go north;go west",
            "武当派-广场": "jh fam 1 start;",
            "武当派-三清殿": "jh fam 1 start;go north",
            "武当派-石阶": "jh fam 1 start;go west",
            "武当派-练功房": "jh fam 1 start;go west;go west",
            "武当派-太子岩": "jh fam 1 start;go west;go northup",
            "武当派-桃园小路": "jh fam 1 start;go west;go northup;go north",
            "武当派-舍身崖": "jh fam 1 start;go west;go northup;go north;go east",
            "武当派-南岩峰": "jh fam 1 start;go west;go northup;go north;go west",
            "武当派-乌鸦岭": "jh fam 1 start;go west;go northup;go north;go west;go northup",
            "武当派-五老峰": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup",
            "武当派-虎头岩": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup;go northup",
            "武当派-朝天宫": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup;go northup;go north",
            "武当派-三天门": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup;go northup;go north;go north",
            "武当派-紫金城": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup;go northup;go north;go north;go north",
            "武当派-林间小径": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup;go northup;go north;go north;go north;go north;go north",
            "武当派-后山小院": "jh fam 1 start;go west;go northup;go north;go west;go northup;go northup;go northup;go north;go north;go north;go north;go north;go north",
            "少林派-广场": "jh fam 2 start;",
            "少林派-山门殿": "jh fam 2 start;go north",
            "少林派-东侧殿": "jh fam 2 start;go north;go east",
            "少林派-西侧殿": "jh fam 2 start;go north;go west",
            "少林派-天王殿": "jh fam 2 start;go north;go north",
            "少林派-大雄宝殿": "jh fam 2 start;go north;go north;go northup",
            "少林派-钟楼": "jh fam 2 start;go north;go north;go northeast",
            "少林派-鼓楼": "jh fam 2 start;go north;go north;go northwest",
            "少林派-后殿": "jh fam 2 start;go north;go north;go northwest;go northeast",
            "少林派-练武场": "jh fam 2 start;go north;go north;go northwest;go northeast;go north",
            "少林派-罗汉堂": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go east",
            "少林派-般若堂": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go west",
            "少林派-方丈楼": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go north",
            "少林派-戒律院": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go north;go east",
            "少林派-达摩院": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go north;go west",
            "少林派-竹林": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go north;go north",
            "少林派-藏经阁": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go north;go north;go west",
            "少林派-达摩洞": "jh fam 2 start;go north;go north;go northwest;go northeast;go north;go north;go north;go north;go north",
            "华山派-镇岳宫": "jh fam 3 start;",
            "华山派-苍龙岭": "jh fam 3 start;go eastup",
            "华山派-舍身崖": "jh fam 3 start;go eastup;go southup",
            "华山派-峭壁": "jh fam 3 start;go eastup;go southup;jumpdown",
            "华山派-山谷": "jh fam 3 start;go eastup;go southup;jumpdown;go southup",
            "华山派-山间平地": "jh fam 3 start;go eastup;go southup;jumpdown;go southup;go south",
            "华山派-林间小屋": "jh fam 3 start;go eastup;go southup;jumpdown;go southup;go south;go east",
            "华山派-玉女峰": "jh fam 3 start;go westup",
            "华山派-玉女祠": "jh fam 3 start;go westup;go west",
            "华山派-练武场": "jh fam 3 start;go westup;go north",
            "华山派-练功房": "jh fam 3 start;go westup;go north;go east",
            "华山派-客厅": "jh fam 3 start;go westup;go north;go north",
            "华山派-偏厅": "jh fam 3 start;go westup;go north;go north;go east",
            "华山派-寝室": "jh fam 3 start;go westup;go north;go north;go north",
            "华山派-玉女峰山路": "jh fam 3 start;go westup;go south",
            "华山派-玉女峰小径": "jh fam 3 start;go westup;go south;go southup",
            "华山派-思过崖": "jh fam 3 start;go westup;go south;go southup;go southup",
            "华山派-山洞": "jh fam 3 start;go westup;go south;go southup;go southup;break bi;go enter",
            "华山派-长空栈道": "jh fam 3 start;go westup;go south;go southup;go southup;break bi;go enter;go westup",
            "华山派-落雁峰": "jh fam 3 start;go westup;go south;go southup;go southup;break bi;go enter;go westup;go westup",
            "华山派-华山绝顶": "jh fam 3 start;go westup;go south;go southup;go southup;break bi;go enter;go westup;go westup;jumpup",
            "峨眉派-金顶": "jh fam 4 start",
            "峨眉派-庙门": "jh fam 4 start;go west",
            "峨眉派-广场": "jh fam 4 start;go west;go south",
            "峨眉派-走廊": "jh fam 4 start;go west;go south;go west",
            "峨眉派-休息室": "jh fam 4 start;go west;go south;go east;go south",
            "峨眉派-厨房": "jh fam 4 start;go west;go south;go east;go east",
            "峨眉派-练功房": "jh fam 4 start;go west;go south;go west;go west",
            "峨眉派-小屋": "jh fam 4 start;go west;go south;go west;go north;go north",
            "峨眉派-清修洞": "jh fam 4 start;go west;go south;go west;go south;go south",
            "峨眉派-大殿": "jh fam 4 start;go west;go south;go south",
            "峨眉派-睹光台": "jh fam 4 start;go northup",
            "峨眉派-华藏庵": "jh fam 4 start;go northup;go east",
            "逍遥派-青草坪": "jh fam 5 start",
            "逍遥派-林间小道": "jh fam 5 start;go east",
            "逍遥派-练功房": "jh fam 5 start;go east;go north",
            "逍遥派-木板路": "jh fam 5 start;go east;go south",
            "逍遥派-工匠屋": "jh fam 5 start;go east;go south;go south",
            "逍遥派-休息室": "jh fam 5 start;go west;go south",
            "逍遥派-木屋": "jh fam 5 start;go north;go north",
            "逍遥派-地下石室": "jh fam 5 start;go down;go down",
            "丐帮-树洞内部": "jh fam 6 start",
            "丐帮-树洞下": "jh fam 6 start;go down",
            "丐帮-暗道": "jh fam 6 start;go down;go east",
            "丐帮-破庙密室": "jh fam 6 start;go down;go east;go east;go east",
            "丐帮-土地庙": "jh fam 6 start;go down;go east;go east;go east;go up",
            "丐帮-林间小屋": "jh fam 6 start;go down;go east;go east;go east;go east;go east;go up",
            "杀手楼-大门": "jh fam 7 start",
            "杀手楼-大厅": "jh fam 7 start;go north",
            "杀手楼-暗阁": "jh fam 7 start;go north;go up",
            "杀手楼-铜楼": "jh fam 7 start;go north;go up;go up",
            "杀手楼-休息室": "jh fam 7 start;go north;go up;go up;go east",
            "杀手楼-银楼": "jh fam 7 start;go north;go up;go up;go up;go up",
            "杀手楼-练功房": "jh fam 7 start;go north;go up;go up;go up;go up;go east",
            "杀手楼-金楼": "jh fam 7 start;go north;go up;go up;go up;go up;go up;go up",
            "杀手楼-书房": "jh fam 7 start;go north;go up;go up;go up;go up;go up;go up;go west",
            "杀手楼-平台": "jh fam 7 start;go north;go up;go up;go up;go up;go up;go up;go up",
            "襄阳城-广场": "jh fam 8 start",
            "武道塔": "jh fam 9 start"
            }
    sm_array = {
        '武当派': {
            'place': "武当派-三清殿",
            'npc': "武当派第二代弟子 武当首侠 宋远桥",
            'sxplace': "武当派-太子岩",
            'sx': "首席弟子"
        },
        '华山派': {
            'place': "华山派-镇岳宫",
            'npc': "市井豪杰 高根明",
            'sxplace': "华山派-练武场",
            'sx': "首席弟子"
        },
        '少林派': {
            'place': "少林派-天王殿",
            'npc': "少林寺第三十九代弟子 道觉禅师",
            'sxplace': "少林派-练武场",
            'sx': "大师兄"
        },
        '逍遥派': {
            'place': "逍遥派-青草坪",
            'npc': "聪辩老人 苏星河",
            'sxplace': "-jh fam 5 start;go west",
            'sx': "首席弟子"
        },
        '丐帮派': {
            'place': "丐帮-树洞下",
            'npc': "丐帮七袋弟子 左全",
            'sxplace': "丐帮-破庙密室",
            'sx': "首席弟子"
        },
        '峨眉派': {
            'place': "峨眉派-大殿",
            'npc': "峨眉派第四代弟子 静心",
            'sxplace': "峨眉派-广场",
            'sx': "大师姐"
        },
        '武馆': {
            'place': "扬州城-扬州武馆",
            'npc': "武馆教习",
            'sxplace': "扬州城-扬州武馆"
        },
        '杀手楼': {
            'place': "杀手楼-大厅",
            'npc': "杀手教习 何小二",
            'sxplace': "杀手楼-练功房",
            'sx': "金牌杀手"
        }
    }

    def __init__(self, serverip, acctoken, palyer=""):
        self.serverip = serverip
        self.acctoken = acctoken
        self.palyer = palyer

    def convet_json(self, json_str):
        json_obj = eval(json_str, type('Dummy', (dict,), dict(__getitem__=lambda s, n: n))())
        return json_obj

    def logCat(self, msg):
        print("{0}: {1}: {2}".format(time.time(), self.myname, msg))

    def go(self, ws, addr):
        if self.addr[addr] is not None:
            sendcmd(ws, self.addr[addr])

    def sm(self, ws):
        while self.mp == '':
            time.sleep(1)
        self.go(ws, self.sm_array[self.mp]['place'])
        self.sfname = self.sm_array[self.mp]['npc']
        time.sleep(1)
        self.logCat(self.smflag)
        while self.smflag:
            time.sleep(1)
            ws.send("task sm " + self.smid)

    def baozi(self, ws):
        self.go(ws, '扬州城-醉仙楼')
        time.sleep(1)
        ws.send("list " + self.dxerid)
        time.sleep(1)
        ws.send("sell all")
        time.sleep(0.5)
        ws.send("buy 20 " + self.baoziid + " from " + self.dxerid)
        time.sleep(1)

    def richang(self, ws):
        if self.rc:
            return
        time.sleep(1)
        ws.send("jh fb 0 start1")
        time.sleep(1)
        ws.send("cr cd/wen/damen")
        time.sleep(1)
        ws.send("cr")
        time.sleep(1)
        ws.send("cr over")
        time.sleep(1)
        ws.send("taskover signin")

    def fuben(self, ws):
        ws.send('pack')
        time.sleep(5)
        for i in range(10):
            time.sleep(1)
            self.richang(ws)
        for i in range(5):
            time.sleep(1)
            if self.rc:
                return
            ws.send("use " + self.yjdid)
        for i in range(10):
            time.sleep(1)
            self.richang(ws)

    def zhuibu(self, ws):
        self.go(ws, '扬州城-衙门正厅')
        while self.zbid == "":
            time.sleep(1)
        ws.send('ask1 ' + self.zbid)
        time.sleep(1)
        ws.send('ask2 ' + self.zbid)
        time.sleep(1)
        ws.send('shop 0 20')
        ws.send('ask3 ' + self.zbid)

    def wakuang(self, ws):
        self.go(ws, "扬州城-矿山")
        time.sleep(1)
        ws.send("wa")

    def lianxi(self, ws, e):
        if e['dialog'] == 'list':
            self.getitemsId(ws, e)
        if e['dialog'] == "skills":
            self.logCat("技能 " + e['id'] + " 提升到 " + str(e['exp']) + "%")
            if 'level' in e:
                # self.logCat(e)
                self.logCat("升级了" + "技能 " + e['id'] + "到" + str(e['level']) + "级")
        if self.yjdid == "":
            if e['dialog'] == "pack":
                if 'items' in e:
                    for item in e['items']:
                        # self.logCat(item)
                        if "养精丹" in item['name']:
                            self.yjdid = item['id']
                            self.logCat("养精丹id:" + self.yjdid)
                            break
        if self.mp == '':
            if e['dialog'] == 'score':
                self.mp = e['family']

    def getsmid(self, ws, e):
        if 'items' in e:
            for item in e["items"]:
                # self.logCat(item)
                if item == 0:
                    continue
                if self.smid == '':
                    if self.sfname in item["name"]:
                        self.smid = item['id']
                        self.logCat("师门id:" + self.smid)
                        break
                if self.dxerid == '':
                    if self.dxename in item["name"]:
                        self.dxerid = item['id']
                        self.logCat("店小二id:" + self.dxerid)
                        break
                if self.zbid == '':
                    if '扬州知府 程药发' in item['name']:
                        self.zbid = item['id']
                        self.logCat("程药发id" + self.zbid)

    def getitemsId(self, ws, e):
        if self.dxerid == '':
            return
        if 'seller' in e:
            self.logCat("getbaozi")
            if e['seller'] == self.dxerid:
                self.logCat("getbaozi1")
                for sellitem in e['selllist']:
                    if sellitem == 0:
                        continue
                    if self.baoziid == "":
                        if "包子" in sellitem['name']:
                            self.baoziid = sellitem['id']
                            self.logCat("包子id:" + self.baoziid)
                            break

    def smcmd(self, ws, e):
        self.logCat(e['items'][0]['cmd'])
        ws.send(e['items'][0]['cmd'])

    def relive(self, ws, e):
        ws.send('relive')
        self.die = True

    def login(self, ws):
        ws.send(self.acctoken)
        ws.send("login " + self.palyer)
        time.sleep(1)
        ws.send('setting ban_pk 1')
        ws.send("stopstate")
        ws.send('pack')
        ws.send("taskover signin")
        ws.send('score')
        time.sleep(1)
        self.logCat("3")
        time.sleep(1)
        self.logCat("2")
        time.sleep(1)
        self.logCat("1")
        time.sleep(1)
        ws.send('tm aa')
        time.sleep(1)

    def getmyname(self, ws, e):
        if e['ch'] == 'tm' and e['uid'] == self.palyer:
            self.myname = e['name']

    def on_message(self, message):
        if "{" and "}" in message:
            e = self.convet_json(message)
            self.logCat(e)
            if e['type'] == "dialog":
                self.lianxi(self.ws, e)
            if e['type'] == "cmds":
                self.smcmd(self.ws, e)
            if e['type'] == "items":
                self.getsmid(self.ws, e)
            if e['type'] == "msg":
                self.getmyname(self.ws, e)
        else:
            self.logCat(message)
            if "你今天已经签到了" in message:
                self.rc = True
            if "休息一下吧" in message:
                self.smflag = False
            if "灵魂状态" in message:
                self.relive(self.ws, message)

    def on_error(self, ws, error):
        self.logCat(error)

    def on_close(self):
        self.logCat("### closed ###")

    def on_open(self, ws):
        def run(*args):
            time.sleep(1)
            self.login(ws)
            self.logCat(self.rc)
            while True:
                if not self.rc:
                    print('rc')
                    self.baozi(ws)
                    self.sm(ws)
                    self.fuben(ws)
                if not self.die:
                    break
            self.zhuibu(ws)
            self.wakuang(ws)
            ws.close()
            self.logCat("thread terminating...")

        thread.start_new_thread(run, ())

    def start(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(self.serverip,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open(self.ws)
        self.ws.run_forever()




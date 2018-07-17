import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import re
class wsgame:
    smflag = True
    yjdid = ''
    smid =''
    rc = False
    sfname = "苏星河"
    dxerid = ''
    dxename = "店小二"
    baoziid = ''
    serverip=''
    acctoken = ''
    palyer =''
    def __init__(self, serverip, acctoken, palyer,sfname):
      self.serverip = serverip
      self.acctoken=acctoken
      self.palyer = palyer
      self.sfname=sfname

    def quote_keys_for_json(self,json_str):
        quote_pat = re.compile(r'".*?"')
        a = quote_pat.findall(json_str)
        json_str = quote_pat.sub('@', json_str)
        key_pat = re.compile(r'(\w+):')
        json_str = key_pat.sub(r'"\1":', json_str)
        assert json_str.count('@') == len(a)
        count = -1
        def put_back_values(match):
            nonlocal count
            count += 1
            return a[count]
        json_str = re.sub('@', put_back_values, json_str)
        return json_str
    
        
    def sm(self,ws):
        ws.send("jh fam 5 start")
        time.sleep(1)
        print(self.smflag)
        while self.smflag:
            time.sleep(1)
            ws.send("task sm "+self.smid)

    def baozi(self,ws):
        ws.send("jh fam 0 start")
        time.sleep(1)
        ws.send("go north")
        time.sleep(1)
        ws.send("go north")
        time.sleep(1)
        ws.send("go east")
        time.sleep(1)
        ws.send("list "+self.dxerid)
        time.sleep(1)
        ws.send("sell all")
        time.sleep(0.5)
        ws.send("buy 20 "+self.baoziid+" from "+self.dxerid)
        time.sleep(1)

    def richang(self,ws):
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

    def fuben(self,ws):
        for i in range(10):
            time.sleep(1)
            self.richang(ws)
        for i in range(5):
            time.sleep(1)
            if self.rc:
                return
            ws.send("use "+self.yjdid)
        for i in range(10):
            time.sleep(1)
            self.richang(ws)
            
            
    def wakuang(self,ws):
        ws.send("jh fam 0 start")
        time.sleep(1)
        ws.send("go west")
        time.sleep(1)
        ws.send("go west")
        time.sleep(1)
        ws.send("go west")
        time.sleep(1)
        ws.send("go west")
        time.sleep(1)
        ws.send("wa")
        
    def lianxi(self,ws,e):
        if e['dialog']=='list':
            self.getitemsId(ws,e)
        if e['dialog']=="skills":
            print("技能 "+e['id'] +" 提升到 "+ str(e['exp'])+"%")
            if 'level' in e:
                #print(e)
                print("升级了"+"技能 "+e['id'] +"到"+str(e['level'])+"级")
        if self.yjdid =="":
            if e['dialog']=="pack":
                if 'items' in e:
                    for item in e['items']:
                        print(item)
                        if "养精丹" in item['name']:
                            self.yjdid = item['id']
                            print("养精丹id:"+self.yjdid)
                            break
    def getsmid(self,ws ,e):
        if 'items' in e:
            for item in e["items"]:
                #print(item)
                if item==0:
                    continue
                if self.smid =='':
                    if self.sfname in item["name"]:
                        self.smid = item['id']
                        print("师门id:"+self.smid)
                        break
                if self.dxerid =='':
                    if self.dxename in item["name"]:
                        self.dxerid = item['id']
                        print("店小二id:"+self.dxerid)
                        break
    def getitemsId(self,ws,e):
        if self.dxerid == '':
            return
        if 'seller' in e:
            print("getbaozi")
            if e['seller'] == self.dxerid:
                print("getbaozi1")
                for sellitem in e['selllist']:
                    if sellitem ==0:
                        continue
                    if self.baoziid =="":
                        if "包子" in sellitem['name']:
                            self.baoziid =sellitem['id']
                            print("包子id:"+self.baoziid)
                            break
                    
    def smcmd(self,ws,e):
        print(e['items'][0]['cmd'])
        ws.send(e['items'][0]['cmd'])
        
    def on_message(self,ws, message):
        if "{" and "}" in message: 
            d = self.quote_keys_for_json(message)
            #print(d)
            e = json.loads(d)
            if e['type']=="dialog":
                self.lianxi(ws,e)
            if e['type']=="cmds":
                self.smcmd(ws,e)
            if e['type']=="items":
                self.getsmid(ws,e)
        else:
            print(message)
            if "你今天已经签到了" in message:
                self.rc = True
            if "休息一下吧" in message:
                self.smflag = False
                
                
    def on_error(self,ws, error):
        print(error)

    def on_close(self,ws):
        print("### closed ###")

    def on_open(self,ws):
        def run(*args):
            time.sleep(1)
            ws.send(self.acctoken)
            #ws.send("login 0f6124bda4e")
            ws.send("login "+self.palyer)
            time.sleep(1)
            ws.send("stopstate")
            ws.send('pack')
            ws.send("taskover signin")
            time.sleep(1)
            print("3")
            time.sleep(1)
            print("2")
            time.sleep(1)
            print("1")
            print(self.rc)
            if not self.rc:
                self.baozi(ws)
                self.sm(ws)
                self.fuben(ws)
            self.wakuang(ws)
            #ws.close()
            print("thread terminating...")
        thread.start_new_thread(run, ())

    def start(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.serverip,
                                on_message = self.on_message,
                                  on_error = self.on_error,
                                  on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()

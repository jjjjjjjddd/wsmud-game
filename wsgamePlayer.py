#edit by knva
#tool VSCODE
#time 2018-8-2 10:12:27
import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time
import json
import re

class wsgamePlayer:
    userlist = []
    static = True
    def __init__(self, serverip, acctoken):
        self.serverip = serverip
        self.acctoken=acctoken

    def convet_json(self,json_str):
        json_obj = eval(json_str, type('Dummy', (dict,), dict(__getitem__=lambda s,n:n))())
        return json_obj

    def on_message(self,ws, message):
        #print(message)
        pobj = self.convet_json(message)
        if(pobj['type']=='roles'):
            for item in pobj['roles']:
                self.userlist.append(item['id'])
            self.static=False

    def on_error(self,ws, error):
        print(error)

    def on_close(self,ws):
        print("### socket closed ###")

    def on_open(self,ws):
        def run(*args):
            ws.send(self.acctoken)
            time.sleep(1)
            ws.close()
            print("获取角色列表成功")
        thread.start_new_thread(run, ())
    def start(self):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.serverip,
                              on_message = self.on_message,
                              on_error = self.on_error,
                              on_close = self.on_close)
        ws.on_open = self.on_open
        ws.run_forever()
    def getList(self):
        return self.userlist
    def getStatic(self):
        return self.static
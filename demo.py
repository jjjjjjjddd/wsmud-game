#edit by knva
#tool VSCODE
#time 2018-8-2 10:12:27
from wsgame import wsgame
from wsgamePlayer import wsgamePlayer
import threading
import time
from wsgameLogin import GetLoginCookie
class MyThread(threading.Thread):
    def __init__(self,serverip,acctoken,player,sfname):
        super(MyThread, self).__init__()
        self.serverip=serverip
        self.acctoken =acctoken
        self.player=player
        self.sfcode=sfname
    def run(self):
        wsg = wsgame(self.serverip,self.acctoken,self.player,self.sfcode)
        wsg.start()

if __name__ == "__main__":
    #填服务器ip 默认1区
    serverurl = "ws://120.78.75.229:25631"
    #参数1:用户名
    #参数2:密码
    c = GetLoginCookie('','')
    utoken =c.getCookie()
    #参数1:服务器url
    #参数2:用户accesstoken
    wsp =  wsgamePlayer(serverurl,utoken)
    
    wsp.start()
    while(wsp.getStatic()):
        time.sleep(1)
    userlist = wsp.getList()
    for pid in userlist:
        #参数1:服务器ip #参数2:用户accesstoken #参数3:pid #参数4:师门id
        #1武当 2少林 3华山 4峨眉 5逍遥 6丐帮
        wsg2= MyThread(serverurl,utoken,pid,5)
        wsg2.start()
        time.sleep(1)
    
    time.sleep(100000)
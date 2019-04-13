#edit by knva
#tool VSCODE
#time 2018-8-2 10:12:27
from wsgame import wsgame
from wsgamePlayer import wsgamePlayer
import threading
import time
from wsgameLogin import GetLoginCookie

class MyThread(threading.Thread):
    def __init__(self, serverip, acctoken, player):
        super(MyThread, self).__init__()
        self.serverip = serverip
        self.acctoken = acctoken
        self.player = player

    def run(self):
        wsg = wsgame(self.serverip, self.acctoken, self.player)
        wsg.start()


if __name__ == "__main__":
    # 填服务器ip 默认1区
    serverurl = "ws://120.79.75.160:25631/"
    # 参数1:用户名
    # 参数2:密码
    c = GetLoginCookie('', '')
    utoken = c.getCookie()
    if utoken== '':
        print('账号密码错误')
        exit(0)
    # 参数1:服务器url
    # 参数2:用户accesstoken
    wsp = wsgamePlayer(serverurl, utoken)

    wsp.start()
    while (wsp.getStatic()):
        time.sleep(1)
    userlist = wsp.getList()
    for pid in userlist:
        # 参数1:服务器ip #参数2:用户accesstoken #参数3:pid
        wsg2 = MyThread(serverurl, utoken, pid)
        wsg2.start()
        time.sleep(1)

    time.sleep(100000)
#edit by knva
#tool VSCODE
#time 2018-8-2 10:12:27
import urllib.request
import urllib.parse
from http import cookiejar
class GetLoginCookie:
    u=''
    p=''
    def __init__(self,username,password):
        self.username = username
        self.password =password
        self.post()
    def getCookie(self):
        return self.u +' '+self.p
    def post(self):
        cookie = cookiejar.CookieJar()
        post_url='http://game.wsmud.com/UserAPI/Login'
        handler = urllib.request.HTTPCookieProcessor(cookie) #创建cookie处理对象
        opener = urllib.request.build_opener(handler) #构建携带cookie的打开方式
        data = {'code':self.username,'pwd':self.password}
        data = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request(post_url,data,method = 'POST') #创建请求
        html = opener.open(req).read() #开启请求,保存登录cookie
        for item in cookie:
            if(item.name=='p'):
                self.p=item.value
            if(item.name=='u'):
                self.u=item.value
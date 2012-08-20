import sys
import urllib.request
import urllib.parse
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:3128','http': '127.0.0.1:3128'})
opener = urllib.request.build_opener(proxy_handler)
site='http://login.vk.com?act=login'
post=urllib.parse.urlencode({'q':'1',
                             'al_frame':'1',
                             'from_host':'vk.com',
                             'act' : 'login',
                             'email' :'',
                             'pass':''})
post=post.encode(encoding='utf_8')
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
                   'Connection' : 'close',
                   'Pragma' : 'no-cache',
                   'Cache-Control' : 'no-cache',
                  }
req=urllib.request.Request(site,post,headers)
#data=opener.open(req)
data=urllib.request.urlopen(req)
#data=opener.open('http://m.vk.com',data=None)
html=data.read().decode(encoding='cp1251')
start=html.index('''setCookieEx('sid',''')
homeB=html.index('''parent.onLoginDone(\'''')
homeE=html[homeB:].index(');')
home=html[homeB+20:homeB+homeE-1]
#print(html)
cookie=html[start+18:start+80] #наша кука
#print(cookie)
req=urllib.request.Request('http://vk.com'+home,None,headers)
req.add_header('Cookie','remixchk=5; '+cookie,
               'remixsid='+cookie+';')
data=urllib.request.urlopen(req)
html=data.read().decode('cp1251')
print(html)
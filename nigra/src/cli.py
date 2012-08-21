import sys
import urllib.request
import urllib.parse
import re
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:3128','http': '127.0.0.1:3128'})
opener = urllib.request.build_opener(proxy_handler)
site='https://login.vk.com?act=login'
post=urllib.parse.urlencode({'q':'1',
                             'al_frame':'1',
                             'from_host':'vk.com',
                             'act' : 'login',
                             'email' :'',#login
                             'pass':''})#pass
post=post.encode(encoding='utf_8')
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
                   'Connection' : 'close',
                   'Pragma' : 'no-cache',
                   'Cache-Control' : 'no-cache',
                  }
req=urllib.request.Request(site,post,headers)
data=opener.open(req)
#data=urllib.request.urlopen(req)
#data=opener.open('http://m.vk.com',data=None)
html=data.read().decode(encoding='cp1251')
#print(html)
home=re.search(r'''(?<=parent.onLoginDone\(\')/\w+''',html).group()#BLOOD FOR THE REGEX GOOOOD!11
#sid=re.search(r'''(?<='sid', ')\w+''',html).group()# OBEY REGEX!!!
cookie=re.search(r"remixsid=\w+;", str(data.info())).group() #ФАК ЙЕА REGEX!!!!1111111
print(cookie)
post=urllib.parse.urlencode({'s':home})
post=post.encode(encoding='utf_8')
#post=None
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
                   'Host' : 'vkontakte.ru',
                   'Referer' : 'http://login.vk.com/?act=login',
                   'Connection' : 'close',
                   'Cookie' : 'remixchk=5;'+cookie,
                   'Pragma' : 'no-cache',
                   'Cache-Control' : 'no-cache'
                  }
#наши куки не для скуки
site='http://vk.com'
req=urllib.request.Request(site,post,headers)
#data=urllib.request.urlopen(req)
data=opener.open(req)
html=data.read().decode('cp1251')

print(data.info())
print(html)
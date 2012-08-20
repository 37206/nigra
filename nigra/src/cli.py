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
                             'email' :'a37206@gmail.com',#login
                             'pass':'upyachka'})#pass
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
#print(html)
home=re.search(r'''(?<=parent.onLoginDone\(\')/\w+''',html).group()#BLOOD FOR THE REGEX GOOOOD!11
sid=re.search(r'''(?<='sid', ')\w+''',html).group()# OBEY REGEX!!!
print(sid)



post=urllib.parse.urlencode({'s':str(sid)})
post=post.encode(encoding='utf_8')
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
                   'Host' : 'vkontakte.ru',
                   'Referer' : 'http://login.vk.com/?act=login',
                   'Connection' : 'close',
                   'Cookie' : 'remixchk=5; remixsid=nonenone',
                   'Pragma' : 'no-cache',
                   'Cache-Control' : 'no-cache'
                  }
#наши куки не для скуки
site='http://vk.com?op=slogin'
req=urllib.request.Request(site,post,headers)
data=urllib.request.urlopen(req)
html=data.read().decode('cp1251')
#cookie=re.sub(r"expires=.+\sdomain=.+",'', str(data.info())) #ФАК ЙЕА REGEX!!!!1111111
print(str(data.info()))
print(html)
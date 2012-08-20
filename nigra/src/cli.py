import sys
import urllib.request
import urllib.parse
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:3128','http': '127.0.0.1:3128'})
opener = urllib.request.build_opener(proxy_handler)
site='http://login.vk.com'
post=urllib.parse.urlencode({'email' :'','pass':''})
post=post.encode(encoding='utf_8')
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
                   'Connection' : 'close',
                   'Pragma' : 'no-cache',
                   'Cache-Control' : 'no-cache',
                  }
req=urllib.request.Request(site,post,headers)
data=opener.open(req)
#data=opener.open('http://m.vk.com',data=None)
print(data.getheaders())
data=opener.open('http://m.vk.com',data=None)
print(data.read().decode(encoding='utf_8'))
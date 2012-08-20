import sys
import urllib.request
import urllib.parse
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:3128','http': '127.0.0.1:3128'})
opener = urllib.request.build_opener(proxy_handler)
req=urllib.parse.urlencode({'email' :'','pass':''})
req=req.encode(encoding='utf_8')
data=opener.open('http://m.vk.com',req)
data=opener.open('http://m.vk.com',data=None)
print(data.getheaders())
print(data.read().decode(encoding='utf_8'))
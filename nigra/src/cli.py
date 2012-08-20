import urllib.request
import sys
proxy_handler = urllib.request.ProxyHandler({'https':'127.0.0.1:3128','http': '127.0.0.1:3128'})
opener = urllib.request.build_opener(proxy_handler)
data=opener.open('https://www.google.ru')
print(data.read())
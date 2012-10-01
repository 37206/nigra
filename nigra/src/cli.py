import sys
import re
import sqlite3
import collections
import requests
from _pyio import StringIO
con = sqlite3.connect('1.db')
c = con.cursor()



def VkAuth(login=None, password=None):
    '''
    Авторизация вконтактоты по хардкору без API
    proxy={protocol:address} 
    
    '''
    class BaseAuthException(Exception): pass
    class LoginIsNone(BaseAuthException): pass
    class PasswordIsNone(BaseAuthException): pass
    global req
    try:
        for name in ('password', 'login'):
            exec("if {0} is None:\n\traise {1}IsNone()".format(name, name.capitalize()))
    except BaseAuthException as err:
        for name in ('Password', 'Login'):
            exec("if isinstance(err,{0}IsNone):\n\tprint('VkAuth() Error: {0} is empty')".format(name))
        return None
    site = 'http://login.vk.com'#https!=squid
    post = {'q':'1', 'al_frame':'1', 'from_host':'vk.com', 'act' : 'login', 'email' :login, 'pass':password}
    data= req.post(site,params=post,allow_redirects=True)
    try:
        home = re.search(r'''(?<=parent.onLoginDone\(\'/)\w+''', data.text).group() #BLOOD FOR THE REGEX GOOOOD!11
    except AttributeError:
        print('VkAuth() Error: Authentication failed')
        return None      
    cookies =data.cookies
    req=requests.session(headers=headers,cookies=cookies,proxies=proxy)
    return 0

def group_search(keywords, cookie):
    '''
    парсер групп по ключевым словам, лол
    '''
    from html.parser import HTMLParser
    parser = HTMLParser()
    s = ''
    for word in keywords:
        s += word + ' '
    site = 'http://vk.com/al_groups.php'#поиск группы 
#    site='http://vk.com/al_video.php'# а вот там лежит хэш для видосов
    post = {'act':'server_search', 'al':'1', 'q':s}#волшебный пост
#    post={'act':'show','al':'1','module':'vieo','video':'100457938_162516488'}
    data = req.post(site,post)  
    html = parser.unescape(data.text)
#    print(html)
#    sys.exit
    html_pre = html.strip().splitlines()
    groups = []
    line = 'd'
    group_stat = collections.namedtuple('group_stat', ['path', 'name', 'num'])
    nstr = 0
    for line in html_pre:
        line = line.lstrip()
        if line.lstrip().startswith('<div class="group_row_labeled"><a href='):
            #еще немного волшебства
            temp1 = re.search(r'(?<=<div class="group_row_labeled"><a href=")/\w+', line).group()
            temp2 = re.sub(r'<.+?>', '', line)
            nstr = 1
        elif nstr == 1:
            nstr = 2
        elif nstr == 2:
            groups.append(group_stat(temp1, temp2, re.search(r'\d+', line).group()))
            nstr = 0
    return groups


def VkUpload(files, type):
    '''грузилка изображений, например
    '''
    if type is 'photo':
        site = 'http://m.vk.com/album11888818_161787398'#поправить на что-то вменяемое
        post = {'s':'','act':'add','from':'select'}
        data = req.post(site,post,allow_redirects=True)  
        html = data.text
        site = re.search(r'''(?<=<form action=")[^"]+''', html).group() #наш урл для загрузки фотачекк, мяффф
        out=dict(('file'+str(i+1),open(file,'rb') if file is not None  else StringIO('')) for i,file in enumerate(files))
        data=req.post(site,files=out,allow_redirects=True)
        resp=re.findall(r'''(?<=<a class="al_photo" href=")[^"]+''', data.text)
        
        
    
    return resp


def parse_news(groups=None):
    for group in groups:
        print('void')



proxy = {'http':'127.0.0.1:3128', 'https':'127.0.0.1:3128'}
proxy = None
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.666; Hail Satan!; rv:1.9.0.1337) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
                       'Pragma' : 'no-cache',
                       'Cache-Control' : 'no-cache',
                      }
req=requests.session(headers=headers,proxies=proxy)

login = ('a37206@gmail.com', 'upyachka')
params = VkAuth(*login)
file = ['./1.jpg',None,None]


found = group_search(['сага', 'сумерки', 'затмение'], params)    
print(found)
type='photo'
found=VkUpload(file, type)
#print(found)
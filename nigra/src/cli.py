import sys
import re
import sqlite3
import collections
import requests
con = sqlite3.connect('1.db')
c = con.cursor()
# Create table
#c.execute('''create table stocks
#(date text, trans text, symbol text,
# qty real, price real)''')

# Insert a row of data
#c.execute("""drop table stocks""")
# Save (commit) the changes
con.commit()

# We can also close the cursor if we are done with it
c.close()



def VkAuth(login=None, password=None):
    '''
    Авторизация вконтактоты по хардкору без API
    proxy={protocol:address} 
    
    '''
    class BaseAuthException(Exception): pass
    class LoginIsNone(BaseAuthException): pass
    class PasswordIsNone(BaseAuthException): pass
    site = 'https://login.vk.com?act=login'
    try:
        for name in ('password', 'login'):
            exec("if {0} is None:\n\traise {1}IsNone()".format(name, name.capitalize()))
    except BaseAuthException as err:
        for name in ('Password', 'Login'):
            exec("if isinstance(err,{0}IsNone):\n\tprint('VkAuth() Error: {0} is empty')".format(name))
        return None
    post = {'q':'1', 'al_frame':'1', 'from_host':'vk.com', 'act' : 'login', 'email' :login, 'pass':password}
#    post = requests.utils.(encoding='utf_8')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
                       'Connection' : 'close',
                       'Pragma' : 'no-cache',
                       'Cache-Control' : 'no-cache',
                      }
    #rewrite
    data = requests.post(site, params=post,headers=headers,proxies=proxy,allow_redirects=True)
#    data = requests.post(site, params=post, headers=headers, proxies=proxy)
#    data = urllib.request.urlopen(req)
#    requests.Request.response.
#    html = data.read().decode(encoding='cp1251')
    try:
        home = re.search(r'''(?<=parent.onLoginDone\(\'/)\w+''', data.text).group() #BLOOD FOR THE REGEX GOOOOD!11
    except AttributeError:
        print('VkAuth() Error: Authentication failed')
        return None      
    print(data.cookies)  
    cookie =data.cookies['remixsid']
#    post = urllib.parse.urlencode({'s':''})
#    post = post.encode(encoding='utf_8')
    params = collections.namedtuple('params', ['cookie', 'home'])
    return params(cookie, home)

def group_search(keywords, cookie):
    '''
    парсер групп по ключевым словам, лол
    '''
    from html.parser import HTMLParser
    parser = HTMLParser()
    s = ''
    for word in keywords:
        s += word + ' '
    print(s)
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
                           'Host' : 'vk.com',
                           'Referer' : 'http://vk.com/groups',
                           'Connection' : 'close',
                           'Cookie' : 'remixchk=5;' + 'remixsid='+params.cookie+';',
                           'Pragma' : 'no-cache',
                           'Cache-Control' : 'no-cache'
                          }
    
    site = 'http://vk.com/al_groups.php'#поиск группы 
    post = {'act':'server_search', 'al':'1', 'q':s}#волшебный пост
#    req = urllib.request.Request(site, post, headers)
    data = requests.post(site,post,headers=headers,proxies=proxy)  
    html = parser.unescape(data.text)
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
            print()
            groups.append(group_stat(temp1, temp2, re.search(r'\d+', line).group()))
            nstr = 0
    return groups


def VkUpload(file, params):
    '''грузилка изображений, например
    '''
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
                       'Host' : 'vk.com',
                       'Referer' : 'http://vk.com/',
                       'Connection' : 'close',
                       'Cookie' : 'remixchk=5;' + params.cookie,
                       'Pragma' : 'no-cache',
                       'Cache-Control' : 'no-cache'
                      }
    #post = urllib.parse.urlencode({'act':'server_search', 'al':'1', 'q':s})#волшебный пост
    site = 'http://m.vk.com/album11888818_161787398?act=add&from=select'
#    post = urllib.parse.urlencode({'s':''}).encode(encoding='utf_8')
#    req = urllib.request.Request(site, post, headers)
#    data = urllib.request.urlopen(req)  
    html = data.read().decode('cp1251')
    site = re.search(r'''(?<=<form action=")[^"]+''', html).group() #наш урл для загрузки фотачекк, мяффф
    print(params.home.lstrip('id'))
    site = 'http://vk.com/al_wall.php'
    post = urllib.parse.urlencode({'act': 'post',
      'type': 'photos_upload',
      'to_id': params.home.strip('id'),
      'attach1_type': 'photos_list',
      'attach1': open(file, 'rb'),
      'hash': hash})
    post = post.encode(encoding='utf_8')
    req = urllib.request.Request(site, post, headers)
    data = urllib.request.urlopen(req)  
    html = data.read().decode('cp1251')
#    print(html)






proxy = {'http':'127.0.0.1:3128', 'https':'127.0.0.1:3128'}
proxy = None
#if proxy is not None: 
#    proxy_handler = urllib.request.ProxyHandler(proxy)
#    opener = urllib.request.build_opener(proxy_handler)
#    urllib.request.install_opener(opener)
login = ('', '')
params = VkAuth(*login)
print(params)
file = './1.jpg'
#VkUpload(file,coo)

#
##===================
#headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
#                       'Host' : 'vkontakte.ru',
#                       'Referer' : 'http://vk.com/groups',
#                       'Connection' : 'close',
#                       'Cookie' : 'remixchk=5;' + coo,
#                       'Pragma' : 'no-cache',
#                       'Cache-Control' : 'no-cache'
#                      }
##========================
#site = 'http://vk.com/feed'
#post = urllib.parse.urlencode({'s':''})
#post = post.encode(encoding='utf_8')
#req = urllib.request.Request(site, post, headers)
#data = urllib.request.urlopen(req)
#html = data.read().decode('cp1251')





found = group_search(['самые', 'котятки', 'милые'], params)    
print(found)
#VkUpload(file, params)

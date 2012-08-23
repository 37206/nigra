import sys
import urllib.request
import urllib.parse
import re
import sqlite3
import collections
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



def VkAuth(proxy=None, login=None, password=None):
    '''
    Авторизация вконтактоты по хардкору без API
    proxy={protocol:address} 
    
    '''
    class BaseAuthException(Exception): pass
    class LoginIsNone(BaseAuthException): pass
    class PasswordIsNone(BaseAuthException): pass
    if proxy is not None: 
        proxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    site = 'https://login.vk.com?act=login'
    try:
        for name in ('password', 'login'):
            exec("if {0} is None:\n\traise {1}IsNone()".format(name, name.capitalize()))
    except BaseAuthException as err:
        for name in ('Password', 'Login'):
            exec("if isinstance(err,{0}IsNone):\n\tprint('VkAuth() Error: {0} is empty')".format(name))
        return None
    post = urllib.parse.urlencode({'q':'1',
                                 'al_frame':'1',
                                 'from_host':'vk.com',
                                 'act' : 'login',
                                 'email' :login,
                                 'pass':password})
    post = post.encode(encoding='utf_8')
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13 (.NET CLR 3.5.30729)',
                       'Connection' : 'close',
                       'Pragma' : 'no-cache',
                       'Cache-Control' : 'no-cache',
                      }
    req = urllib.request.Request(site, post, headers)   
    data = urllib.request.urlopen(req)
    html = data.read().decode(encoding='cp1251')
    try:
        home = re.search(r'''(?<=parent.onLoginDone\(\')/\w+''', html).group() #BLOOD FOR THE REGEX GOOOOD!11
    except AttributeError:
        print('VkAuth() Error: Authentication failed')
        return None        
    cookie = re.search(r"remixsid=\w+;", str(data.info())).group() #ФАК ЙЕА REGEX!!!!1111111
    post = urllib.parse.urlencode({'s':''})
    post = post.encode(encoding='utf_8')
    params=collections.namedtuple('params',['cookie', 'home'])
    return params(cookie,home)

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
                           'Cookie' : 'remixchk=5;' + params.cookie,
                           'Pragma' : 'no-cache',
                           'Cache-Control' : 'no-cache'
                          }
    
    site = 'http://vk.com/al_groups.php'#поиск группы 
    post = urllib.parse.urlencode({'act':'server_search', 'al':'1', 'q':s})#волшебный пост
    post = post.encode(encoding='utf_8')
    req = urllib.request.Request(site, post, headers)
    data = urllib.request.urlopen(req)  
    html = parser.unescape(data.read().decode('cp1251'))
    html_pre = html.strip().splitlines()
    groups = []
    line = 'd'
    group_stat=collections.namedtuple('group_stat', ['path','name','num'])
    nstr=0
    for line in html_pre:
        line = line.lstrip()
        if line.lstrip().startswith('<div class="group_row_labeled"><a href='):
            #еще немного волшебства
            temp1=re.search(r'(?<=<div class="group_row_labeled"><a href=")/\w+', line).group()
            temp2=re.sub(r'<.+?>','', line)
            nstr=1
        elif nstr==1:
            nstr=2
        elif nstr==2:
            print()
            groups.append(group_stat(temp1,temp2,re.search(r'\d+',line).group()))
            nstr=0
    return groups


def VkUpload(file,params):
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
    site='http://vk.com'
    #post = urllib.parse.urlencode({'act':'server_search', 'al':'1', 'q':s})#волшебный пост
    post = urllib.parse.urlencode({'s':''})
    post = post.encode(encoding='utf_8')
    req = urllib.request.Request(site, post, headers)
    data = urllib.request.urlopen(req)  
    html = data.read().decode('cp1251')
    hash=re.search(r'''(?<="post_hash":")\w+''',html).group()
    print(hash)
    
    post = urllib.parse.urlencode({'file':open(file, 'rb'),      'act': 'post',
      'type': 'photos_upload',
      'to_id': params.home,
      'attach1_type': 'photos_list',
      'attach1': 'photos',
      'hash': hash} )
    post = post.encode(encoding='utf_8')
    site='http://cs315522.vk.com/upload.php'
    req = urllib.request.Request(site, post, headers)
    data = urllib.request.urlopen(req)  
    html = data.read().decode('cp1251')
    print(html)






proxy = {'http':'127.0.0.1:3128', 'https':'127.0.0.1:3128'}
#proxy = None
login = ('a37206@gmail.com', 'upyachka')
params = VkAuth(proxy, *login)
print(params)
file='./1.jpg'
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





found=group_search(['самые', 'котятки', 'милые'], params)    
VkUpload(file, params)

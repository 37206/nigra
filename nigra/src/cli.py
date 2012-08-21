import sys
import urllib.request
import urllib.parse
import re
import sqlite3
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



def VkAuth(proxy=None,login=None,password=None):
    '''
    proxy={protocol:address}
        
    
    '''
    class BaseAuthException(Exception): pass
    class LoginIsNone(BaseAuthException): pass
    class PasswordIsNone(BaseAuthException): pass
#    class AuthFailed(Exception): pass 
    if proxy is not None: 
        proxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxy_handler)
        urllib.request.install_opener(opener)
    site = 'https://login.vk.com?act=login'
    try:
        for name in ('password','login'):
            exec("if {0} is None:\n\traise {1}IsNone()".format(name,name.capitalize()))

    
    
    
#        if login is None:
#            raise LoginIsNone()
#        if password is None:
#            raise PasswordIsNone()
    except BaseAuthException as err:
        for name in ('Password','Login'):
            exec("if isinstance(err,{0}IsNone):\n\tprint('VkAuth() Exception: {0} is empty')".format(name))
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
    #data=urllib.request.urlopen(req)
    #data=opener.open('http://m.vk.com',data=None)
    html = data.read().decode(encoding='cp1251')
    #print(html)
    home = re.search(r'''(?<=parent.onLoginDone\(\')/\w+''', html).group() #BLOOD FOR THE REGEX GOOOOD!11
    #sid=re.search(r'''(?<='sid', ')\w+''',html).group()# OBEY REGEX!!!
    cookie = re.search(r"remixsid=\w+;", str(data.info())).group() #ФАК ЙЕА REGEX!!!!1111111
    if cookie is None:
        print('nya!')
        
    post = urllib.parse.urlencode({'s':home})
    post = post.encode(encoding='utf_8')
    #post=None
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13',
                       'Host' : 'vkontakte.ru',
                       'Referer' : 'http://login.vk.com/?act=login',
                       'Connection' : 'close',
                       'Cookie' : 'remixchk=5;' + cookie,
                       'Pragma' : 'no-cache',
                       'Cache-Control' : 'no-cache'
                      }
    #наши куки не для скуки
    site = 'http://vk.com'
    req = urllib.request.Request(site, post, headers)
    #data=urllib.request.urlopen(req)
    data = opener.open(req)
    html = data.read().decode('cp1251')
    return cookie
proxy={'http':'127.0.0.1:3128','https':'127.0.0.1:3128'}
login=(None,None)
coo=VkAuth(proxy, *login)
print(coo)
#coding=UTF-8
import json
import requests
import random
import time
from yzb_db_connect import *
from yzb_conf import config as conf
# from fanqie_ip import fanqie_ip_list




#黑洞代理
def proxy_ip4():
    proxy_url = 'http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=7&fa=1&groupid=0&fetch_key=&qty=20&time=100&port=1&format=json&ss=5&css=&ipport=1&pro=&city=&dt=1&usertype=4'
    html = requests.get(proxy_url).json()
    print(html,type(html))
    ip_list = html['data']
    return ip_list


#精灵代理
def proxy_ip3():
    proxy_url = 'http://t.11jsq.com/index.php/api/entry?method=proxyServer.generate_api_url&packid=1&fa=0&fetch_key=&groupid=0&qty=20&time=1&pro=&city=&port=1&format=json&ss=5&css=&ipport=1&dt=1&specialTxt=3&specialJson=&usertype=2'
    html = requests.get(proxy_url).json()
    # print(html,type(html))
    ip_list = html['data']
    return ip_list


#快代理
def proxy_ip2():
    proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num=10&pt=1&dedup=1&format=json&sep=1'
    # proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num=10&pt=1&format=json&sep=1'
    html = requests.get(proxy_url,headers={'Accept-Encoding': 'gzip'}).json()
    # print(html,type(html))
    if html['code'] == 0 and html['data']['today_left_count'] > 0:
        ip_list = html['data']['proxy_list']
        print(ip_list)

        return ip_list


#快代理，自定义数量
def proxy_ip(num):
    proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num={}&pt=1&dedup=1&format=json&sep=1'.format(str(num))
    # proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num=10&pt=1&format=json&sep=1'

    html = requests.get(proxy_url,headers={'Accept-Encoding': 'gzip'}).json()
    print(html,type(html))
    if html['code'] == 0 and html['data']['today_left_count'] > 0:
        ip_list = html['data']['proxy_list']
        print(ip_list)

        return ip_list


#快代理，自定义数量
def proxy_sock_ip(num):
    proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num={}&pt=2&dedup=1&format=json&sep=1'.format(str(num))
    # proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num=10&pt=1&format=json&sep=1'
    html = requests.get(proxy_url,headers={'Accept-Encoding': 'gzip'}).json()
    # print(html,type(html))
    if html['code'] == 0 and html['data']['today_left_count'] > 0:
        ip_list = html['data']['proxy_list']
        print(ip_list)

        return ip_list


def proxy_ip_one():
    proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num=1&pt=1&dedup=1&format=json&sep=1'
    # proxy_url = 'https://dps.kdlapi.com/api/getdps/?orderid=998338810310271&num=10&pt=1&format=json&sep=1'
    html = requests.get(proxy_url,headers={'Accept-Encoding': 'gzip'}).json()
    print(html,type(html))
    if html['code'] == 0 and html['data']['today_left_count'] > 0:
        ip_list = html['data']['proxy_list']
        print(ip_list)

        return ip_list


def proxy_sock_list(ip_list):
    proxies = {
        'http': 'socks5://%(proxy)s' % {'proxy': random.choice(ip_list)},
        'https': 'socks5://%(proxy)s' % {'proxy': random.choice(ip_list)}
    }
    return proxies


def proxy_list(ip_list):

    # 精灵代理
    # proxies = {
    #     "http": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)['IP']},
    #     "https": "https://%(proxy)s/" % {'proxy': random.choice(ip_list)['IP']}
    # }


    #快代理
    proxies = {
        # "http": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)},
        "https": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)}
    }
    # print(proxies)
    return proxies


def proxy_amount_white(ip_list):
    # 快代理
    proxies = {
        "http": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)},
        # "https": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)}
    }
    # print(proxies)
    return proxies

def proxy_amount_pwd(ip_list):
    # 通过密码
    username = "agua1101"
    password = "pgftac5x"
    proxies = {
        "http": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": random.choice(ip_list)},
        # "https": "http://%(user)s:%(pwd)s@%(proxy)s/" % {"user": username, "pwd": password, "proxy": random.choice(ip_list)}
    }
    # print(proxies)
    return proxies


def proxy_amount(ip_list):
    sever_ip = conf.server
    if not sever_ip:
        return proxy_amount_white(ip_list)
    else:
        return proxy_amount_pwd(ip_list)




def proxy_list_https(ip_list):
    proxies = {
        # "http": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)},
        "https": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)}
    }
    # print(proxies)
    return proxies


def proxy_fanqie():
    proxies = {
        # "http": "http://%(proxy)s/" % {'proxy': random.choice(fanqie_ip_list)},
        # "https": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)}
    }
    # print(proxies)
    return proxies




def proxy_orderly(ip_list,p=0):
    proxies = {
        "http": "http://%(proxy)s/" % {'proxy': ip_list[p]},
        # "https": "http://%(proxy)s/" % {'proxy': random.choice(ip_list)}
    }
    # print(proxies)
    return proxies



def proxy_ip_fanqie():
    proxy_url = 'http://x.fanqieip.com/index.php?s=/Api/IpManager/adminFetchFreeIpRegionInfoList&uid=12668&ukey=5df550d6a7e8739cf8c5a9c67ddf1483&limit=10&format=0&page=1'
    html = requests.get(proxy_url).json()
    print(html)




#小象代理
def proxy_ip1():
    proxy_url = 'http://api.xiaoxiangdaili.com/ip/get?appKey=546663031627993088&appSecret=DgB4hn8j&cnt=&wt=json'
    html = requests.get(proxy_url).json()
    print(html)
    ip = html['data'][0]['ip']
    port = html['data'][0]['port']
    proxy = {'http':ip+':'+str(port)}
    return proxy


#云代理
# def proxy_ip():
#     proxy_url = 'http://gec.ip3366.net/api/?key=20200214165224100&getnum=30&filter=1&area=1&formats=2'
#     html = requests.get(proxy_url).content.decode('GB18030')
#     proxy_tough = json.loads(html)
#     # print(type(proxy_list),proxy_list)
#     proxy_list = []
#     for i in proxy_tough:
#         # proxy_list.append({'http':'{}:{}'.format(i["Ip"],i["Port"])})
#         proxy_list.append('{}:{}'.format(i["Ip"],i["Port"]))
#
#     return proxy_list

def ex_proxy(proxy_list):
    proxies = random.choice(proxy_list)
    return proxies




def test_ip(p_list):

    try:
        # print(p_list)
        requests.adapters.DEFAULT_RETRIES = 3
        IP = random.choice(p_list)
        thisProxy = IP['http']
        thisIP = "".join(thisProxy.split(":")[0])
        # print(thisIP)
        res = requests.get(url="http://icanhazip.com/", timeout=8, proxies={"http": thisProxy})
        proxyIP = res.text
        print(proxyIP)
        print(thisIP)
        if (proxyIP == thisIP):
            print("代理IP:'" + proxyIP + "'有效！")
        else:
            print("代理IP无效！")
    except:
        print("代理IP无效！")





# test_url = 'https://www.baidu.com/'
# timeout = 60
# def test_proxy(proxy):
#     try:
#         proxies = {'https': 'http://' + proxy}
#         start_time = time.time()
#         requests.get(test_url, timeout=timeout, proxies=proxies)
#         end_time = time.time()
#         used_time = end_time - start_time
#         print('Proxy Valid', 'Used Time:', used_time)
#         return True, used_time
#     except (ProxyError, ConnectTimeout, SSLError, ReadTimeout, ConnectionError):
#         print('Proxy Invalid:', proxy)
#         return False, None

def valVer(proxys):
    badNum = 0
    goodNum = 0
    good=[]
    for proxy in proxys:
        try:
            proxy_host = proxy
            protocol = 'https' if 'https' in proxy_host else 'http'
            proxies = {protocol: proxy_host}
            print('现在正在测试的IP：',proxies)
            response = requests.get('http://www.zycg.gov.cn/article/show/548411', proxies=proxies, timeout=2)
            if response.status_code != 200:
                badNum += 1
                print (proxy_host, 'bad proxy')
            else:
                goodNum += 1
                good.append(proxies)
                print (proxy_host, 'success proxy')
        except Exception as e:
            print(e)
            # print proxy_host, 'bad proxy'
            badNum += 1
            continue
    print ('success proxy num : ', goodNum)
    print( 'bad proxy num : ', badNum)
    print(good)
    return good

def save_good(good_ip_list):
    import json
    d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)
    dict_save = {}
    # ip_list = [{'http': '117.69.50.130:9999'}, {'http': '183.154.52.166:9999'}, {'http': '222.95.144.24:3000'}, {'http': '171.35.149.197:9999'}, {'http': '183.164.239.92:9999'}, {'http': '183.154.49.48:9999'}, {'http': '115.211.226.168:9999'}, {'http': '114.239.3.131:9999'}, {'http': '121.237.148.206:3000'}, {'http': '222.95.240.121:3000'}]
    try:
        for i in good_ip_list:
            ip_key = list(i.keys())[0]
            print(ip_key)
            ip_value = list(i.values())[0]
            print(ip_value)
            notnull_dict(ip_key, dict_save, 'good_ip_key')
            notnull_dict(ip_value, dict_save, 'good_ip_value')
            # dict_save['good_ip_key'] = ip_key
            # dict_save['good_ip_value'] = ip_value
            d_save.insert('t_proxy_ip', dict_save)
        print('save success!')
    except Exception as e:
        print(e)
        print('save fail!')


def good_ip():
    d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)
    ip_list = d_save.select_all('*','t_proxy_ip')
    # print(ip_list)
    good_ip_list = []
    good_ip = {}
    for i in ip_list:
        good_ip[i[1]] = i[2]
        good_ip_list.append(good_ip)
    print(good_ip_list)

    return good_ip_list



def main():
    p_list = proxy_ip()
    # print(p_list)
    good_list = valVer(p_list)
    save_good(good_list)
    time.sleep(5)

def check_ip2():
    a = 'https://dps.kdlapi.com/api/getdpsvalidtime?orderid=998338810310271&signature=a7h5kq49xsgy7eg2wk0uibvqo1qaxj62&proxy=106.6.202.104:22124'
    text = requests.get(a).json()
    print(text)


# 从数据库获取代理IP
def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

# 从数据库删除代理IP
def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))




if __name__ == '__main__':
    ip_list = proxy_ip(8)
    print(ip_list)
    # main()
    # proxy_ip2()
    # check_ip2()
    # proxies = {
    #     "https": "https://%(proxy)s/" % {'proxy': '183.166.147.97:15011'}
    # }
    # print(proxies)
    # # proxy_ip_one()
    # import requests
    # try:
    #     res = requests.get(url='https://www.baidu.com/',proxies=proxies)
    # except:
    #     proxy_one = proxy_ip_one()[0]
    #     proxies = {
    #         "https": "https://%(proxy)s/" % {'proxy': proxy_one}
    #     }
    #     print(proxies)
    #     res = requests.get(url='https://www.baidu.com/', proxies=proxies)
    # # print(res)
    # print(res.status_code,'res_code')
    # # proxy_list(proxy_ip3())

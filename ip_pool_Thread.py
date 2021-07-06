#-*- coding = utf-8 -*-
#@Time :  16:36
#@Author : yuwenhui
#File : ip_pool_Thread.py
#@Software : PyCharm

'''
    "./"：代表目前所在的目录。

    " ../"代表上一层目录。

    "/"：代表根目录。

'''

import requests
from threading import Thread
from lxml import etree
import numpy
import time

proxies = numpy.load('./Proxy_new.npy', allow_pickle=True)
# print(proxies)
ip = numpy.random.choice(proxies)
print(ip)

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'
}

def get_ip():
    proxies_list = []
    for page_num in range(1, 17):
        print("================ getting the page {} now ==============".format(page_num))
        baseurl = "https://www.kuaidaili.com/free/inha/"+str(page_num)
        # baseurl = "https://www.kuaidaili.com/free/inha/{}".format(page_num)   方法2

        resp = requests.get(url=baseurl, headers=headers, proxies=ip)
        page_text = resp.text
        # print(page_text)

        tree = etree.HTML(page_text)
        tr_list = tree.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr')
        # print(tr_list)

        for td in tr_list:
            proxies_dict = {}
            HEAD_TYPE = td.xpath('./td[4]/text()')[0]   # 如果列表只有一个数据   [0] 可以用extract_first()代替
            IP = td.xpath('./td[1]/text()')[0]
            PORT = td.xpath('./td[2]/text()')[0]
            # print(IP, PORT, HEAD_TYPE)
            proxies_dict[HEAD_TYPE] = IP + ":" + PORT
            # print(proxies_dict)
            proxies_list.append(proxies_dict)
        time.sleep(1)

    # print(proxies_list)
    print("over, the num of ip is", len(proxies_list))
    return proxies_list

H_quality_ip = []

def check_ip(proxy):
    try:
        resp = requests.get(url='https://www.baidu.com', headers=headers, proxies=proxy, timeout=0.3)
        if resp.status_code == 200:
            print("ip {} is ok".format(proxy))
            H_quality_ip.append(proxy)
        else:
            print("ip {} is not ok".format(proxy))
    except:
        print("ip {} is not ok".format(proxy))

# 多线程检测
def check_ip_Thread(proxies_list):
    Thread_list = []
    for proxy in proxies_list:
        t = Thread(target=check_ip, args=(proxy,))
        Thread_list.append(t)
        t.start()

    for t in Thread_list:
        t.join()

if __name__ == "__main__":
    proxies_list = get_ip()
    check_ip_Thread(proxies_list)
    print("getting high quality ip is over")
    print(H_quality_ip)
    print("the num of high quality ip is", len(H_quality_ip))
    print("the rate of save is {}%".format(round(len(H_quality_ip)*100/len(proxies_list), 2)))
    numpy.save('./Proxy_new.npy', H_quality_ip)
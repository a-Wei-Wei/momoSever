import requests
from bs4 import BeautifulSoup
import re

def getIps():
    url = "http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
    response = requests.get(url)
    msg = response.text
    # print(msg)
    p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
    iplist = re.findall(p,msg)
    return iplist

def getIpsFromTxt():
    file = open("./ips.txt")
    msg = file.readlines()
    list_temp = []
    for temp in msg:
        temp = temp.replace("\r", "").replace("\n", "")
        list_temp.append(temp)

    return list_temp

def main():
    # ipList = getIps()
    ipList = getIpsFromTxt()
    url = "https://www.maimemo.com/share/page?uid=13225050&pid=b4823f8989f0f4b6ae5c94f42584fbab&tid=98e17a9c378dbe0c29c3c17d565b5a6a"
    for ip_temp in ipList:
        # ip = ip_temp[0]
        # port = ip_temp[1]
        # https_proxy = "{0}:{1}".format(ip, port)
        https_proxy = ip_temp
        proxies={
            'https': https_proxy
        }
        msg = ""
        try:
            response = requests.get(url, proxies=proxies, timeout=5)
            msg = response.text
        except Exception as identifier:
            print("{0} timeOut".format(ip_temp))
        # print(msg)
        if "墨墨" in msg:
            print("{0} , success".format(ip_temp))
        


if __name__ == "__main__":
    main()
    # print(getIpsFromTxt())
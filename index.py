import requests
from bs4 import BeautifulSoup
import re
import configparser
import time

config_parse = configparser.ConfigParser()
config_parse.read("./momoUrl")

#可以用这个方法，就是用免费66代理网站爬下来的 代理ip
def getIps():
    url = "http://www.66ip.cn/mo.php?sxb=&tqsl=100&port=&export=&ktip=&sxa=&submit=%CC%E1++%C8%A1&textarea="
    response = requests.get(url)
    msg = response.text
    # print(msg)
    p = r'(?:((?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5])\.(?:\d|[1-9]\d|1\d{2}|2[0-5][0-5]))\D+?(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9]))'
    iplist = re.findall(p,msg)
    return iplist

#暂时废弃，因为芝麻代理一次性不让获取大于20个的IP
def getIps_form_zima():
  url = config_parse.get("section three","url")
  file = open("./ips.txt", "w")
  res = requests.get(url)
  soup = BeautifulSoup(res.text,"html.parser")
  content = soup.string.replace("\r", "")
  file.write(content)
  time.sleep(2)
  print("ips获取完毕, 共{0}".format(140))
  # print(array_content)

#代替上面的这个函数，反复获取6次。一共120个IP
def getIps_from_zima_with_txt():
  print("=====开始获取IP=====")
  url = config_parse.get("section three", "url_20")
  file = open("./ips.txt", "w")
  for i in range(6):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    content = soup.string.replace("\r", "")
    file.write(content)
    time.sleep(2)
  print("获取IP完毕，共计：{0}".format(6*20))

# 这个函数就是 使用本地文件中获取芝麻代理ip
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
    # getIps_form_zima()
    getIps_from_zima_with_txt()
    ipList = getIpsFromTxt()
    print("开始运行访问服务，其中获取ip池中{0}个IP".format(len(ipList)))
    url = config_parse.get("section one", "url")
    url_2 = config_parse.get("section tow", "url")
    flag_url_2 = False
    for ip_temp in ipList:
        https_proxy = ip_temp
        proxies={
            'https': https_proxy
        }
        msg = ""
        if ip_temp == "" or len(ip_temp) <= 0:
          print("运行完毕")
          continue
        try:
            if url_2 and flag_url_2:
              response = requests.get(url_2, proxies=proxies, timeout=5)
              msg = response.text
              flag_url_2 = False
            else:
              response = requests.get(url, proxies=proxies, timeout=5)
              msg = response.text
              flag_url_2 = True
        except Exception as identifier:
            print("{0} timeOut".format(ip_temp))
        # print(msg)
        if "墨墨" in msg:
            print("{0} , success , {1}".format(ip_temp, flag_url_2))
        


if __name__ == "__main__":
    main()
    # print(getIpsFromTxt())
    # getIps_form_zima()
    # getIps_from_zima_with_txt()

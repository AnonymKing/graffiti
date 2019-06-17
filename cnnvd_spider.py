# -*- coding: utf-8 -*-
# @Author: KING
# @Date:   2019-05-28 11:01:00
# @Last Modified by:   KING
# @Last Modified time: 2019-06-17 09:09:02

import re
import requests
from bs4 import BeautifulSoup

# 获取漏洞详情的连接
DETAIL_URL = 'http://www.cnnvd.org.cn/web/xxk/ldxqById.tag'
# 漏洞查找的连接 用于将CVE编号转换成CNNVD编号以获取漏洞信息
SEARCH_URL = 'http://www.cnnvd.org.cn/web/vulnerability/queryLds.tag'

# 伪造请求头
headers = {
    "Host": "www.cnnvd.org.cn",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "DNT": "1",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Referer": "http://www.cnnvd.org.cn/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


def clear_str(string):
    """@Function 清洗字符串，去掉多余的空白字符"""
    return "".join(string.split())


def is_CVE(cve):
    if re.match('^CVE-[0-9]{4,6}-[0-9]{1,8}$', cve):
        return True
    else:
        return False


def is_CNNVD(cnnvd):
    if re.match('^CNNVD-[0-9]{4,6}-[0-9]{1,6}$', cnnvd):
        return True
    else:
        return False


def get_CNNVD(cnnvd):
    """
    @Param cnnvd  格式为CNNVD-201808-536
    """

    # 获取数据
    params = {'CNNVD': cnnvd}
    r = requests.get(url=DETAIL_URL, params=params, headers=headers)
    if r.status_code != 200:
        return False
    r.encoding = r.apparent_encoding

    # 整理数据
    soup = BeautifulSoup(r.text, 'lxml')
    wrapper = soup.find('div', attrs={"class": "fl w770"})
    detail = wrapper.find('div', attrs={"class": "detail_xq"})
    print("漏洞名称：", clear_str(detail.h2.getText()))
    li = detail.find_all('li')
    for i in li:
        print(clear_str(i.getText()))
    ldjj = clear_str(wrapper.find('div', attrs={'class': 'd_ldjj'}).getText())
    if ldjj[:4] == "漏洞简介":
        ldjj = "漏洞简介：" + ldjj[4:]
        print(ldjj)
    return True


def get_CVE(cve):
    """
    @Param cve  格式为CVE-2019-2247
    """

    # 获取数据
    params = {'qcvCnnvdid': cve}
    r = requests.get(url=SEARCH_URL, params=params, headers=headers)
    if r.status_code != 200:
        return False
    r.encoding = r.apparent_encoding

    # 整理数据
    soup = BeautifulSoup(r.text, 'lxml')
    wrapper = soup.find('div', attrs={"class": "fl w770"})
    div = wrapper.find('div', attrs={"class": "list_list"})
    li = div.ul.find_all('li')
    if len(li) < 1:
        print("Sorry，没有查找到！")
        return False
    elif len(li) > 1:
        print("请输入精确的CVE编号")
        return False
    else:
        # 转换CVE编号为CNNVD编号
        cnnvd = clear_str(li[0].div.p.a.getText())
        if is_CNNVD(cnnvd):
            # 获取漏洞详情
            return get_CNNVD(cnnvd)
        else:
            print("Sorry，没有查找到！")
            return False


def main():
    key_str = str(input("Input CNNVD or CVE ID:")).strip()
    key_str = key_str.upper()
    if key_str in ["Q", "QUIT", "BYE", "EXIT"]:
        print("Bye Bye!")
        return
    if is_CVE(key_str):
        if not get_CVE(key_str):
            print("Something is Wrong @CVE!")
    elif is_CNNVD(key_str):
        if not get_CNNVD(key_str):
            print("Something is Wrong @CNNVD!")
    else:
        print("输入不合法！\n")
    print('\n\n')
    main()


if __name__ == '__main__':
    main()

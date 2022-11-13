# !/usr/bin/python3
# -*- coding: utf8 -*-
from importlib import reload
import io
import sys
import requests
from bs4 import BeautifulSoup
# reload(sys)
# sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
# sys.getdefaultencoding('utf-8')
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') 
#改变标准输出的默认编码 #改变标准输出的默认编码
# html = requests.get('https://www1.szu.edu.cn/mailbox/list.asp?page=1&leader=%BD%A8%D1%D4%CF%D7%B2%DF&tag=').text
# print(html)
# 根据每一页url规律构造出url
def get_url(page):
    head = 'https://www1.szu.edu.cn/mailbox/list.asp?page='
    tail = '&leader=%BD%A8%D1%D4%CF%D7%B2%DF&tag='
    variable = str(page)
    url = head + variable + tail
    return url


def get_title(url):
    # 伪装成浏览器，防止封ip
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.35',
    }
    # 进行认证，不然抓取到的不是真的页面
    # 如果访问不了可能是cookies过期了
    cookies = {
        'ASPSESSIONIDAADTCQBT': 'ANAGALEALKBMFMGIJMHDOECA',
        'ASPSESSIONIDAADSASAS': 'MCCJEPHDAPFIKMIJFAFNHJAG'
    }
    
    tries = 2
    while tries > 0:
        try: 
            rsp = requests.get(url, headers=headers, cookies=cookies)
            break
        except Exception as e:
            tries -= 1
            print(e)
    # 防止中文乱码
    rsp.encoding = rsp.apparent_encoding
    data = rsp.text
    # 生成soup对象进行标签筛选
    soup = BeautifulSoup(data, 'lxml')
    soup_tag = soup.find_all('a', target="_blank" )
    title = []
    for item in soup_tag:
        name = item.text[1::]
        title.append(name)
    title.pop()
    print(title)
    return title

def main():
    title_list = []
    for page in range(1, 243):
        link = get_url(page)
        titles = get_title(link)
        title_list += titles
        # print(title_list)

    # 写入txt文件中
    for title in title_list:
        #这里的文件地址自行更改
        with open('\home\title.txt', 'a', encoding='utf8') as f:
            f.write(title + '\n')


if __name__ == '__main__':
    main()
    

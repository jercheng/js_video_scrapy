import os
import time
import requests
from lxml import etree
import json
import random
import re
from s_my_config import cookies
from user_agent import user_agent_list

from woff import AnalysisFont

font = AnalysisFont()


def str_to_dict(cookie_str):
    cook_dict = {}
    for item in cookie_str.split(";"):
        item1 = item.split("=")
        cook_dict[item1[0].strip()] = item1[1].strip()

    return cook_dict


class MaoyanSpider(object):
    def __init__(self):
        self.start_url = "http://maoyan.com/films?offset={}"
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': '你的cookie',
            'Host': 'maoyan.com',
            'Referer': 'http://maoyan.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
        }

        self.cook_dict_list = [str_to_dict(cookies_item) for cookies_item in cookies]

    def __get_header(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': random.choice(cookies),
            'Host': 'maoyan.com',
            'Referer': 'http://maoyan.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': random.choice(user_agent_list),
        }

    # 电影详情页
    def moive_detail(self, movie_url):
        item = dict()
        html = requests.get(movie_url, headers=self.__get_header()).text
        selector = etree.HTML(html)
        # 猫眼电影 票房和想看人数 是用到了特殊字符加密  页面找到加密文件 解密

        woff_url = selector.xpath('//style/text()')[0].split(';')[2].replace("\n", "")
        woff_url = 'http:' + woff_url.split(',')[1].strip().strip("").strip("format('woff')").strip().split('\'')[1]
        print(woff_url)
        print(self.num_char_woff(woff_url,movie_url))

    def num_char_woff(self,woff_url,movie_url):
        """得到数字映射关系"""
        movie_id = re.sub(r"http://maoyan.com/films/", "", movie_url)
        import io
        r = requests.get(woff_url, headers=self.__get_header())
        # print(r.content)
        data = io.BytesIO(r.content)
        return font.get_num_list(data)


def main():
    url = "http://maoyan.com/films/1208942"

    maoyan = MaoyanSpider()

    maoyan.moive_detail(url)

if __name__ == '__main__':
    main()

import requests
from lxml import etree
import pymysql
import time
import json
import random
from s_my_config import cookies
from user_agent import user_agent_list

def str_to_dict(cookie_str):
    cook_dict = {}
    for item in cookie_str.split(";"):
        item1 = item.split("=")
        cook_dict[item1[0].strip()] = item1[1].strip()

    return cook_dict

class MaoyanSpider(object):
    def __init__(self):
        self.start_url = 'http://maoyan.com/films'
        self.moive_list = []
        self.MYSQL_CONFIG = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': 'admin2016',
            'db': 'local_db',
            'charset': 'utf8'
        }
        self.cook_dict_list = [str_to_dict(cookies_item) for cookies_item in cookies]
        self.same_item = 0
        # self.conn = pymysql.connect(**self.MYSQL_CONFIG)

    def __get_header(self):
       return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': random.choice(cookies),
            'Host': 'maoyan.com',
            'Referer': 'http://maoyan.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent':random.choice(user_agent_list),
        }
    # 解析猫眼电影 请求的url组合 分类 地区 年代
    def parse_urls(self):
        try:
            html = requests.get(self.start_url, headers=self.__get_header()).text
        except:
            time.sleep(10)
            html = requests.get(self.start_url, headers=self.__get_header()).text
        selector = etree.HTML(html)
        infos = selector.xpath(
            '//div[@class="movies-channel"]/div[@class="tags-panel"]/ul[@class="tags-lines"]/li/ul[@class="tags"]/li[position()>1]')
        item = {}
        item['分类'] = []
        item['地区'] = []
        item['年代'] = []
        big_dic = {}
        for type_info in infos:
            href = type_info.xpath('a/@href')[0]
            text = type_info.xpath('a/text()')[0]
            dic = {href: text}
            big_dic[href] = text
            if 'cat' in href:
                type = '分类'
                item[type].append(dic)
            elif 'sourceId' in href:
                type = '地区'
                item[type].append(dic)
            else:
                type = '年代'
                item[type].append(dic)
        all_url = []
        cats = []
        for cat in item['分类']:
            cats.append(list(cat.keys())[0])
        areas = []
        for area in item['地区']:
            areas.append(list(area.keys())[0])
        years = []
        for year in item['年代']:
            years.append(list(year.keys())[0])
        offsets = [str(item*30) for item in range(0,1000000)]
        for cat in cats:
            for area in areas:
                for year in years:
                    for offset in offsets:
                        url = self.start_url + cat + '&' + area.lstrip('?') + '&' + year.lstrip(
                            '?') + '&offset=' + offset
                        tags = big_dic[cat] + "," + big_dic[area] + "," + big_dic[year]
                        all_url.append({'url': url, 'tags': tags})
                       
                        res_code = self.parse_moive({'url': url, 'tags': tags})
                        time.sleep(random.randrange(2,5))
                        if res_code == 3 or res_code == 2:
                            print("\033[1;31m ", res_code,"这个条目找到终点，跳出去~~~" ,url," \033[0m")
                            if res_code == 2:
                                with open("temp1","a",encoding="utf-8") as file_r:
                                    file_r.write(url+"\n")
                            break

        return all_url

    # 根据不同请求 解析出电影的url以及该电影的属性
    def parse_moive(self, item):
        # html = requests.get(item['url'], headers=self.headers).text
        try:
            html = requests.get(item['url'],headers = self.__get_header()).text
        except:
            print("\033[1;31m ", "被发现了 休息60秒 " " \033[0m")
            time.sleep(30)
            try:
                html = requests.get(item['url'], headers=self.__get_header()).text
            except:
                print("\033[1;31m ", "再次被发现!!! 休息180秒 " " \033[0m")
                time.sleep(180)
                html = requests.get(item['url'], headers=self.__get_header()).text
        if """抱歉，没有找到相关结果，请尝试用其他条件筛选。""" in html:
            return 3
        selector = etree.HTML(html)
        infos = selector.xpath(
            '//div[@class="movies-list"]/dl[@class="movie-list"]//div[@class="channel-detail movie-item-title"]/a')

        if len(infos) > 0:
            for info in infos:

                b_same = False

                movie_url = 'http://maoyan.com' + info.xpath('@href')[0]
                movie_name = info.xpath('text()')[0]
                # print(movie_name, movie_url, item['tags'])
                movie_item = {}
                movie_item['movie_name'] = movie_name
                movie_item['movie_url'] = movie_url
                movie_item['tags'] = item['tags']
                movie_item['req_url'] = item['url']

                with open("man_yan_url", "r", encoding="utf-8") as file_r:
                    for item_recoder in file_r.readlines():
                        json_item_recoder = json.loads(item_recoder)
                        if movie_url == json_item_recoder['movie_url'] and item['tags'] == json_item_recoder['tags']:
                            print("\033[1;31m ", "-相同 --->> ",json_item_recoder,'\n',movie_item, " \033[0m")
                            b_same = True
                            self.same_item += 1
                            if self.same_item > 4:
                                self.same_item = 0
                                return 2


                if not b_same:
                    self.insert_moive(movie_item)
            self.same_item = 0

    def insert_moive(self, moive_item):
        # insert_sql='insert into maoyan_moive values(%s,%s,%s,%s)'
        # cursor.execute(insert_sql,(moive_item['movie_name'],moive_item['movie_url'],moive_item['tags'],moive_item['req_url']))
        # print('插入成功')
        # conn.commit()
        with open("man_yan_url", "a", encoding="utf-8") as file_w:
            print("写入 ->", moive_item)
            file_w.write(json.dumps(moive_item,ensure_ascii=False) + "\n")

    def get_moive_list(self, urls):
        for i in range(len(urls)):
            item = urls[i]
            print(i + 1, '------->', item['url'], item['tags'])
            self.parse_moive(item)
            time.sleep(3)


if __name__ == '__main__':
    maoyan = MaoyanSpider()
    # conn = maoyan.conn
    # cursor = conn.cursor()
    all_urls = maoyan.parse_urls()
    # maoyan.get_moive_list(all_urls)
    # cursor.close()
    # conn.close()

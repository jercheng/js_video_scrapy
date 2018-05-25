import requests
from lxml import etree
from user_agent import user_agent_list
import random
import time
from s_my_config import cookies

def str_to_dict(cookie_str):
    cook_dict = {}
    for item in cookie_str.split(";"):
        item1 = item.split("=")
        cook_dict[item1[0].strip()] = item1[1].strip()

    return cook_dict

def generate_url():
    pass

def main():
    cook_dict_list = [str_to_dict(cookies_item) for cookies_item in cookies]
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }
    file_w = open("urls","w",encoding="utf-8")
    for i in range(101,1000000):
        url = "https://maoyan.com/films?offset="+str(i*30)
        try:
            res = requests.get(url,headers = headers,cookies = random.choice(cook_dict_list)).text
        except:
            print("\033[1;31m ", "被发现了 休息60秒 " " \033[0m")
            time.sleep(30)
            try:
                res = requests.get(url, headers=headers,cookies = random.choice(cook_dict_list)).text
            except:
                print("\033[1;31m ", "再次被发现!!! 休息180秒 " " \033[0m")
                time.sleep(180)
                res = requests.get(url, headers=headers,cookies = random.choice(cook_dict_list)).text

        # print(res)
        et = etree.HTML(res)
        r = et.xpath("//*[@class='movie-item']/a/@href")
        # print("https://maoyan.com/".join(r))
        while not len(r):
            print("\033[1;31m ", "有危险！被封了 停止10分钟" " \033[0m")
            time.sleep(600)
            res = requests.get(url, headers=headers, cookies=random.choice(cook_dict_list)).text
            et = etree.HTML(res)
            r = et.xpath("//*[@class='movie-item']/a/@href")
        http_url = ["https://maoyan.com"+item for item in r]
        print(url)
        print(http_url)
        for item in http_url:
            file_w.write(item+"\n")
            file_w.flush()
        rt = random.randrange(8,31)
        print("\033[1;31m ", "随机休息...", rt, " \033[0m")
        time.sleep(rt)

        
        if i % 100 == 0:
            rt = random.randrange(100, 180)
            print("\033[1;31m ", "能被100整除，是个好数字，休息一会儿..", rt, " \033[0m")
            time.sleep(rt)

        
    file_w.close()


if __name__ == '__main__':
    main()
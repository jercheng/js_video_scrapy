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


def main():
    session = requests.session()
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }

    url = "https://maoyan.com/films?offset=819570"


    # res = session.get(url, headers=headers).text
    # print(session.cookies)
    # # print(res)
      # cook_dict = {}
    # for item in cookies.split(";"):
    #     item1 = item.split("=")
    #     cook_dict[item1[0].strip()]=item1[1].strip()

    # print(cook_dict)
    cook_dict_list = [str_to_dict(cookies_item) for cookies_item in cookies]
    # cook_dict = str_to_dict(cookies)

    res = session.get(url, headers=headers,cookies = cook_dict_list[1]).text
    print(res)
    print(session.cookies)

if __name__ == '__main__':
    main()
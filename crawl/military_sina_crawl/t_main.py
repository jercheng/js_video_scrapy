import requests
import json
from lxml import etree
import re
import time

dgjq_url = """http://platform.sina.com.cn/news/news_list?app_key=2872801998&channel=mil&cat_1=dgby&show_all=0&format=json&show_num=500000000"""


def get_clean_string(string1):
    s = re.sub(r"\[(.*)\]", "", string1).replace(" ", "").replace("  ", "")
    s = re.sub(r"\n|\t|\r|,|\u3000|\xa0", "", s)
    return s


def parse_dgjq_news(url, session):
    try:
        res = session.get(url).content.decode('utf-8','ignore')
    except:
        print("\033[1;31m ", "发生故障 休息20秒 " " \033[0m")
        time.sleep(20)
        try:
            res = session.get(url).content.decode('utf-8','ignore')
        except:
            print("\033[1;31m ", "！！！发生严重故障 休息60秒 " " \033[0m")
            print(url)
            time.sleep(60)
            res = session.get(url).content.decode('utf-8','ignore')

    res1 = re.sub(r'<\s*script[^>]*>[^<]*<\s*/\s*script\s*>|<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', "", res)
    # print(res)
    html = etree.HTML(res1)
    sel = html.xpath("//* [@id='artibody']")
    if sel:
        return sel[0].xpath("string(.)")
    else:
        sel = html.xpath("//* [@id='article']")
        if sel:
            return sel[0].xpath("string(.)")


def main():
    file_w = open("dgjq", "w", encoding="utf-8")
    file_e = open("dgjq_error", "w", encoding="utf-8")
    session = requests.session()
    res = session.get(dgjq_url).text
    res_json = json.loads(res)["result"]["data"]
    # print(len(res_json))
    for item in res_json:
        # print(item['url'])
        content = parse_dgjq_news(item['url'], session)
        if content:
            # print(item['title'],get_clean_string(content))
            item["content"] = get_clean_string(content)
            print(item)
            file_w.write(json.dumps(item, ensure_ascii=False) + "\n")
        else:
            file_e.write(json.dumps(item, ensure_ascii=False) + "\n")
    file_w.close()


if __name__ == '__main__':
    main()

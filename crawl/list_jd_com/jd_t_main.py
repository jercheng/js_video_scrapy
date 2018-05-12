import requests
import json
import re
from lxml import etree
import csv

"""
http://list.jd.com/list.html?cat=737,794,798&sort=sort_rank_asc&trans=1&md=1&my=list_brand

"""

url_append = "&sort=sort_rank_asc&trans=1&md=1&my=list_brand"


def parse(url):
    # url = "http://list.jd.com/list.html?cat=737,794,798"

    url = url + url_append
    res = requests.get(url).content.decode("utf-8","ignore")
    # html = etree.HTML(res)
    # print(res)
    # print(html.xpath("//*[@id='brandsArea']/li/a/@title"))
    try:
        res_list = []
        res_json = json.loads(res)['brands']
        for item in res_json:
            print(item)
            res_list.append(item)

        return res_list
    except:
        return None


def main():
    # parse("")
    file_w = open("all_brands.csv", "w", encoding="utf-8", newline="")
    file_csv_w = csv.writer(file_w)
    url = 'https://dc.3.cn/category/get'
    res = requests.get(url)

    data = json.loads(res.content.decode("gbk"))['data']

    for item in data:
        # 主类标签
        cate_c = item['id']
        for second_item in item['s']:
            # item = CateItem()
            # item['main_cate'] = cate_c
            second = second_item['n'].split('|')
            # item['url'] = second[0]
            # item['name'] = second[1]
            # item['child'] = []
            for third_item in second_item['s']:
                third = third_item['n'].split('|')
                if not re.search('list.html', third[0]):
                    third[0] = "http://list.jd.com/list.html?cat=" + third[0].replace('-', ',')

                if not re.search('http://', third[0]):
                    third[0] = "http://" + third[0]
                # tir = {'url':third[0],'name':third[1]}
                # item['child'].append(tir)
                # yield SplashRequest(third[0].strip(),
                #                     meta={'thirdCateName': third[1], 'thirdUrl': third[0], 'secondName': second[1],
                #                           'secondUrl': second[0], 'main_cate': cate_c}, callback=self.parse_item,
                #                     dont_filter=True)

                meta = {'thirdCateName': third[1], 'thirdUrl': third[0], 'secondName': second[1],
                        'secondUrl': second[0], 'main_cate': cate_c, 'url': third[0]}

                res1 = parse(meta['url'])
                # print(meta)
                if res1:
                    for item_brands in res1:
                        result = [second[1], second[0], third[1], third[0], item_brands['id'], item_brands['pinyin'],
                                  item_brands['name'], item_brands['logo']]
                        file_csv_w.writerow(result)

    file_w.close()


if __name__ == '__main__':
    main()

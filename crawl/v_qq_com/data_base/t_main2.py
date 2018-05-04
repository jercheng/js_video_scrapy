from mysql_connect import MysqlConnect
from s_config import config
import requests
import re
import json
import csv
import time
import random


def get_video_type(video_name):
    res = re.findall(r'-(.*)-|_(.*)_', video_name)
    if len(res):
        for item in res[0]:
            if item:
                return item

    else:
        return None


def get_greater_30(v_id,error_file):
    url = "http://s.video.qq.com/get_playsource?id=" + v_id + "&type=4&range=1-10000&otype=json"
    session = requests.session()
    res = session.get(url).text
    json_re = re.match("QZOutputJson=(.*)", res).groups()
    if len(json_re):

        json_res = json.loads(json_re[0][:-1])
        print(url,json_res)

        if not json_res['PlaylistItem'] :
            error_file.write(v_id + "\n")
            return None

        if 'videoPlayList' in json_res['PlaylistItem']:
            return json_res['PlaylistItem']['videoPlayList']
        else:
            error_file.write(v_id+"\n")
            return None

    else:
        error_file.write(v_id + "\n")
        return None


def main():
    video_time = "20180503"
    mc = MysqlConnect(config)
    csv_file_1 = open('data/'+video_time + '_video_greater_30.csv', 'w', newline='', encoding="utf-8")
    csv_writer_1 = csv.writer(csv_file_1)
    csv_file_2 = open('data/'+video_time + '_video_type.csv', 'w', newline='', encoding="utf-8")
    csv_writer_2 = csv.writer(csv_file_2)
    error_file = open('data/'+'error_item','a',encoding='utf-8')
    sql = """select detail_title,detail_pid from tx_jieshaoye where  update_date = """ + video_time + """ and episodes > 30"""

    res = mc.exec_query(sql)
    for item in res:

        re_json = get_greater_30(item[1],error_file)

        if not re_json:
            time.sleep(3)
            re_json = get_greater_30(item[1], error_file) #再请求一次

        if not re_json:
            print("error: ", item[0])
        else:
            csv_writer_2.writerow([item[0], get_video_type(item[0])])
            for ep_item in re_json:
                # print(item[0], get_video_type(item[0]), re_json)
                # if "番外" in ep_item['episode_number'] or int(ep_item['episode_number']) > 30:
                #     print(ep_item['title'], ep_item['playUrl'], ep_item['episode_number'])
                has_no_num = re.findall(r"[^\d]+", ep_item['episode_number'])
                if len(has_no_num) or int(ep_item['episode_number']) > 30:
                    # print(ep_item['title'], ep_item['playUrl'])
                    if len(has_no_num):
                        csv_writer_1.writerow([item[0] + ep_item['title'], ep_item['playUrl']])
                    else:
                        csv_writer_1.writerow([ep_item['title'], ep_item['playUrl']])
    time.sleep(random.randint(1,3))
    csv_file_1.close()
    csv_file_2.close()
    error_file.close()
    mc.close()


if __name__ == '__main__':
    main()

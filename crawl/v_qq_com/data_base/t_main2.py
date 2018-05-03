from mysql_connect import MysqlConnect
from s_config import config
import requests
import re
import json


def get_video_type(video_name):
    res = re.findall(r'-(.*)-', video_name)
    if len(res):
        return res[0]

    else:
        return None


def get_greater_30(v_id):
    url = "http://s.video.qq.com/get_playsource?id=" + v_id + "&type=4&range=1-10000&otype=json"
    session = requests.session()
    res = session.get(url).text
    json_re = re.match("QZOutputJson=(.*)", res).groups()
    if len(json_re):

        json_res = json.loads(json_re[0][:-1])
        return json_res['PlaylistItem']['videoPlayList']

    else:
        return None


def main():
    mc = MysqlConnect(config)

    sql = """select detail_title,detail_pid from tx_jieshaoye where  update_date = '20180425' and episodes > 30"""

    res = mc.exec_query(sql)
    for item in res:
        re_json = get_greater_30(item[1])
        if not re_json:
            print("error: ", item[0])
        else:
            print(item[0], re_json)

    mc.close()


if __name__ == '__main__':
    main()

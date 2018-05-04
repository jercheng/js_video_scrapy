import re
import requests
import json

def get_greater_30(v_id,error_file):
    url = "http://s.video.qq.com/get_playsource?id=" + v_id + "&type=4&range=1-10000&otype=json"
    session = requests.session()
    res = session.get(url).text
    json_re = re.match("QZOutputJson=(.*)", res).groups()
    if len(json_re):

        json_res = json.loads(json_re[0][:-1])
        # print(url,json_res)

        if not json_res['PlaylistItem'] :
            print("111",v_id)
            return None

        if 'videoPlayList' in json_res['PlaylistItem']:
            return json_res['PlaylistItem']['videoPlayList']
        else:
            print("222", v_id)
            return None

    else:
        return None

def main():
    r = get_greater_30("s2fo606divlys5k","")
    print(r)
if __name__ == '__main__':
    main()
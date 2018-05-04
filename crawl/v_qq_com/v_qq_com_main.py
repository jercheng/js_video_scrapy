import requests
import json
import re


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
    # temp_id = "jvhuaf93hh858fs"
    # temp_id = "sx5xljydk45g1pp"
    v_id = "7casb7nes159mrl"
    temp_id = "00v79tmuo39v1va"
    temp_id = "s2fo606divlys5k"
    temp_id = "uv56axs1nx33hmc"
    res = get_greater_30(temp_id)

    for item in res:
        print(item)


if __name__ == '__main__':
    main()

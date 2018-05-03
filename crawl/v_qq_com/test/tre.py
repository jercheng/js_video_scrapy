import re

def main():
    str1 = "游戏幻影（普通话）(Game Maya)-电视剧-腾讯视频"
    res = re.findall(r'-(.*)-|_(.*)_',str1)
    if len(res):
        for item in res[0]:
            if item:
                print(item)

    else:
        print("")


if __name__ == '__main__':
    main()
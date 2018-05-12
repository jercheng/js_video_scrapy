import re


def main():
    str1 = "冀远康（JIYUANKANG）"

    name_china = re.sub("（.*）", "", str1)
    name_english = re.sub(name_china,"",str1)

    print(name_china,name_english[1:-1])

if __name__ == '__main__':
    main()

import os
import re


def get_ch_en(str1):
    name_china = re.sub("（.*）", "", str1)
    name_english = re.sub(name_china, "", str1)

    return (name_china, name_english[1:-1])


def parse(file_name):
    file_r_o = open('second_brands/'+file_name, 'r',encoding='utf-8',errors='ignore')

    file_r = file_r_o.readlines()

    file_w = open('second_brands_2/' + file_name, 'w', encoding='utf-8')

    temp_set = set()

    for item in file_r:
        print(item)
        print(len(item))
        try:
            tem_item = item.strip().split(',')[1].strip()

            if "（" in tem_item and "）" in tem_item:
                print(tem_item)
                ch_en = get_ch_en(tem_item)
                print(ch_en)
                temp_set.add(ch_en[0])
                temp_set.add(ch_en[1])

            else:
                temp_set.add(tem_item)
        except :
            print("----")
            continue

    for item in temp_set:
        file_w.write(item+'\n')

    file_r_o.close()
    file_w.close()


def main():
    pa = os.listdir('second_brands/')
    for item in pa:
        parse(item)


if __name__ == '__main__':
    main()

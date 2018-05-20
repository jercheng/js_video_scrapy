import os
import re

def get_ch_en(str1):
    name_china = re.sub("（.*）", "", str1)
    name_english = re.sub(name_china, "", str1)

    return (name_china, name_english[1:-1])

def main():
    all_brands = open("all_brands.csv","r",encoding="utf-8")
    for item in all_brands.readlines():
        brands_list = item.strip().split(',')
        dir_name = brands_list[0]
        if not os.path.exists("sorted_brands_data/"+dir_name):
            print("创建目录 "+dir_name)
            os.makedirs("sorted_brands_data/"+dir_name)
        file_name = "sorted_brands_data/"+dir_name+"/"+brands_list[2]
        file_temp = open(file_name,"a",encoding="utf-8")

        if "（" in brands_list[7] and "）" in brands_list[7]:
            print(brands_list[7])
            ch_en = get_ch_en(brands_list[7])
            file_temp.write(ch_en[0] + "\n")
            file_temp.write(ch_en[1] + "\n")
        else:
            file_temp.write(brands_list[7]+"\n")

        file_temp.close()


if __name__ == '__main__':
    main()
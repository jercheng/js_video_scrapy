import requests
from user_agent import user_agent_list
import random
from lxml import etree
import re
import os
import time


def get_clean_string(string1):
    s = re.sub(r"\[(.*)\]", "", string1).replace(" ", "").replace("  ", "")
    s = re.sub(r"\n|\t|\r|,", "", s)
    return s


def get_baike_summary(word, error_file_hander, word_lable):
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }
    url = """https://baike.baidu.com/item/""" + word
    try:
        res = requests.get(url, headers=headers).content.decode("utf-8")
    except:
        print("\033[1;31m ", "发生故障 休息10秒 " " \033[0m")
        time.sleep(10)
        res = requests.get(url, headers=headers).content.decode("utf-8")
    if res:
        html = etree.HTML(res)
        sel = html.xpath("//*[@class='lemma-summary']")
        title = html.xpath("//*[@class='lemmaWgt-lemmaTitle-title']/h1/text()")
        if len(sel) and len(title):
            summary_content = sel[0].xpath('string(.)')
            title_content = title[0]
            return [word, title_content, get_clean_string(summary_content)]
        else:
            print(word + " " + "no found")
            error_file_hander.write(word + "\n")
            error_file_hander.flush()
            return None
    else:
        return None


def main():
    # w_items = os.listdir("words")
    w_items = []
    dir = "words"
    for root, dirs, files in os.walk(dir, True):
        # print('root: %s' % root)
        # print('dirs: %s' % dirs)
        # print('files: %s' % files)

        for item in files:
            w_items.append(root.replace('words\\', '') + '/' + item)

    for w_item in w_items:
        # file_name = "app行业词.txt"
        file_name = w_item
        word_label = file_name[:-4]
        cache_words = []
        if os.path.exists("cache/" + file_name):
            cache_words = [item.strip() for item in open("cache/" + file_name, "r", encoding="utf-8").readlines()]
            print("-------------------------")
        cache_file = open("cache/" + file_name, "a", encoding="utf-8")
        error_file = open("error/" + file_name + "_error", "a", encoding="utf-8")
        corpus = open("data/" + file_name + "_corpus.csv", "a", encoding="utf-8")

        words = [item.strip() for item in open("words/" + file_name, "r", encoding="utf-8").readlines()]
        # print(words)
        for word in words:

            if word in cache_words:
                print("\033[1;31m ", word, " done " " \033[0m")
                continue
            else:
                url = """https://baike.baidu.com/item/"""
                # print(random.choice(user_agent_list))
                # error_file = ""
                # word_label = ""
                r = get_baike_summary(word, error_file, word_label)
                # corpus.write(r.join(","))
                if r:
                    print(','.join(r))
                    corpus.write(','.join(r) + "\n")
                    corpus.flush()

                else:
                    pass

                cache_words.append(word)
                cache_file.write(word + "\n")
                cache_file.flush()
                # error_file.close()

        cache_file.close()
        error_file.close()
        corpus.close()


if __name__ == '__main__':
    main()

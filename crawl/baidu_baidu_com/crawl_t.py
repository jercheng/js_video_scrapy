import requests
from user_agent import user_agent_list
import random
from lxml import etree
import re
import os


def get_clean_string(string1):
    s = re.sub(r"\[(.*)\]", "", string1).replace(" ","").replace("  ","")
    s = re.sub(r"\n|\t|\r|,", "", s)
    return s


def get_baike_summary(word, error_file_hander, word_lable):
    headers = {
        'User-Agent': random.choice(user_agent_list)
    }
    url = """https://baike.baidu.com/item/""" + word
    res = requests.get(url, headers=headers).content.decode("utf-8")
    html = etree.HTML(res)
    sel = html.xpath("//*[@class='lemma-summary']")
    title = html.xpath("//*[@class='lemmaWgt-lemmaTitle-title']/h1/text()")
    if len(sel) and len(title):
        summary_content = sel[0].xpath('string(.)')
        title_content = title[0]
        return [word, title_content, get_clean_string(summary_content)]
    else:
        print(word + " " + "no found")
        return None
        # error_file_hander.write(word+"\n")


def main():
    file_name = "3c行业词.txt"
    if os.path.exists("cache/"+file_name):
        cache_words = [item.strip() for item in open("words/" + file_name, "r", encoding="utf-8").readlines()]
        print("---")
    else:

    words = [item.strip() for item in open("words/"+file_name,"r",encoding="utf-8").readlines()]
    # print(words)
    for word in words:
        url = """https://baike.baidu.com/item/"""
        print(random.choice(user_agent_list))
        word_label = ""
        error_file = open("error/"+word_label+"_error","w",encoding="utf-8")
        corpus = open("data/"+word_label+"_corpus","w",encoding="utf-8")

        # error_file = ""
        # word_label = ""
        r = get_baike_summary(word,error_file,word_label)
        # corpus.write(r.join(","))
        if r:
            print(','.join(r))
            corpus.write(','.join(r)+"\n")
        else:
            pass
        # error_file.close()



if __name__ == '__main__':
    main()

import json

def main():
    with open("man_yan_url","r",encoding="utf-8")as file_r,open("clear_movie_url","w",encoding="utf-8") as file_w:
        movie_url_set = set()
        index = 1
        for item in file_r.readlines():
            json_item = json.loads(item.strip())
            movie_url_set.add(json_item['movie_url'])
            
            
            print("480126",index,float(index/480126),"%")
            index += 1
            
        
        for item in movie_url_set:
            file_w.write(item+"\n")
            
        
            
        
if __name__ == '__main__':
    main()
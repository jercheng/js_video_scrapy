import json
import sys

def main():
    with open("man_yan_url","r",encoding="utf-8") as file_r,open("clear_url","w",encoding="utf-8") as file_w:
        clear_movie = []
        index = 1
        for item in file_r.readlines():
            json_item = json.loads(item.strip())
            is_not_in = True
            for item_movie in clear_movie:
                if item_movie['movie_url'] == json_item['movie_url']:
                    is_not_in = False
                    break

            print("480126",index,float(index/480126),"%")
            if is_not_in:
                clear_movie.append(json_item)
                file_w.write(item)

            index += 1

        print(clear_movie)
        print(len(clear_movie))




if __name__ == '__main__':
    main()
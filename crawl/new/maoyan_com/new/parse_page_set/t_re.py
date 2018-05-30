import re

def main():
    url = """http://maoyan.com/films/1208942"""

    r = re.sub(r"http://maoyan.com/films/","",url)
    print(r)

if __name__ == '__main__':
    main()
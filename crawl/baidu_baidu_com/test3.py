import os
import datetime


def main():
    while True:
        re = os.system("python crawl_t2.py")
        now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if re:
            print("\033[1;31m ", now_time, "发生故障 " " \033[0m")
        if re == 0:
            print("\033[1;31m ", now_time, "^_^ 执行完成 " " \033[0m")
            break


if __name__ == '__main__':
    main()

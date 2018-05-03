from mysql_connect import MysqlConnect
from s_config import config
def main():
    mc = MysqlConnect(config)


if __name__ == '__main__':
    main()
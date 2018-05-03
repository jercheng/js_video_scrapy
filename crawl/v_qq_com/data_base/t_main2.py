from mysql_connect import MysqlConnect
from s_config import config
def main():
    mc = MysqlConnect(config)

    sql = """ select * from tx_jieshaoye"""

    res = mc.exec_query(sql)
    print(res)

    mc.close()


if __name__ == '__main__':
    main()
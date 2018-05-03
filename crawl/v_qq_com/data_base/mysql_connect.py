import pymysql
from sshtunnel import SSHTunnelForwarder


class MysqlConnect:
    def __init__(self, config):
        # self.server = SSHTunnelForwarder(
        #     ssh_address_or_host=('10.10.10.179', 8404),
        #     ssh_password="VwKyQMEDnXb5n6Kx",
        #     ssh_username="zhangmaohong",
        #     remote_bind_address=('127.0.0.1', 3306)
        # )

        self.server = SSHTunnelForwarder(
            ssh_address_or_host=(config["ssh_host"], config["ssh_port"]),
            ssh_password=config["ssh_pwd"],
            ssh_username=config["ssh_user_name"],
            remote_bind_address=(config['target_host'], config['target_port'])
        )

        self.server.start()
        # print(server.local_bind_port)
        # self.client = pymysql.connect(host='127.0.0.1',
        #                               port=self.server.local_bind_port,
        #                               user='inst',
        #                               passwd='inst@123456ZMH',
        #                               db='video_data',
        #                               charset='utf8')

        self.client = pymysql.connect(host='127.0.0.1',
                                      port=self.server.local_bind_port,
                                      user=config['sql_user'],
                                      passwd=config['sql_pwd'],
                                      db=config['db'],
                                      charset='utf8')

        self.cur = self.client.cursor()

    def exec_query(self, sql):
        cur = self.cur
        cur.execute(sql)
        res = cur.fetchall()
        self.client.commit()
        return res

    def close(self):
        self.cur.close()
        self.server.close()

import pymysql
from sshtunnel import SSHTunnelForwarder


def main():
    server = SSHTunnelForwarder(
        ssh_address_or_host=('10.10.10.179', 8404),
        ssh_password="VwKyQMEDnXb5n6Kx",
        ssh_username="zhangmaohong",
        remote_bind_address=('127.0.0.1', 3306)
    )

    server.start()
    print(server.local_bind_port)
    client = pymysql.connect(host='127.0.0.1',
                             port=server.local_bind_port,
                             user='inst',
                             passwd='inst@123456ZMH',
                             db='video_data',
                             charset='utf8')

    cursor = client.cursor()

    sql = """ select * from tx_jieshaoye"""

    rel = cursor.execute(sql)

    rel = cursor.fetchall()

    client.commit()
    print(rel)
    print("---")
    cursor.close()

    server.close()


if __name__ == '__main__':
    main()

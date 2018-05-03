import pymysql
from sshtunnel import SSHTunnelForwarder


def main():
    server = SSHTunnelForwarder(
        ssh_address_or_host=('', 8404),
        ssh_password="",
        ssh_username="",
        remote_bind_address=('', 3306)
    )

    server.start()
    print(server.local_bind_port)
    client = pymysql.connect(host='127.0.0.1',
                             port=server.local_bind_port,
                             user='',
                             passwd='',
                             db='',
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

import pymysql
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', charset='utf8')
conn.cursor().execute("DROP DATABASE bookstore")
conn.cursor().execute("CREATE DATABASE bookstore")
conn.commit()

import pymysql

db = pymysql.connect(host="localhost", user="root", passwd="1234", db="furniture", charset="utf8")
cur = db.cursor()

# 가구 테이블 조회
def furniture():
    sql = "SELECT * FROM furniture"
    cur.execute(sql)
    furniture_list = cur.fetchall()
    return furniture_list

# 가구분류 테이블 조회
def furniture_classification():
    sql = "SELECT * FROM furniture_classification"
    cur.execute(sql)
    furniture_classification_list = cur.fetchall()
    return furniture_classification_list
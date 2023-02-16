import pymysql
from model import *
import config.config as conf

class DAO():
    def __init__(self):
        self.conn = None

    def connect(self):        
        self.conn = pymysql.connect(host=conf.db['host'], user=conf.db['user'], passwd=conf.db['password'],
                                    db="furniture", charset="utf8")

    def disconnect(self):
        self.conn.close()


    # 가구 테이블 조회
    def furniture(self):
        self.connect()
        cur = self.conn.cursor()

        sql = "SELECT * FROM furniture"
        cur.execute(sql)
        furniture_list = cur.fetchall()

        self.conn.commit()
        self.disconnect()

        return furniture_list

    # 가구분류 테이블 조회
    def furniture_classification(self):
        self.connect()
        cur = self.conn.cursor()

        sql = "SELECT * FROM furniture_classification"
        cur.execute(sql)
        furniture_classification_list = cur.fetchall()
    
        self.conn.commit()
        self.disconnect()
     
        return furniture_classification_list



    def getProduct(self, productIdx):
        # TODO: Dao 에서 데이터 받아오기 #########
        productName = "이름"
        productPrice = 1234
        productDescrip = "설명"
        productUrl = "링크"
        #####################################

        getProductRes = GetProductRes(productIdx, productName, productPrice, productDescrip, productUrl)

        return getProductRes


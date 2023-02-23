import pymysql
from model import *
import config.config as conf
from config.BaseResponse import *

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
        try:
            self.connect()
            cur = self.conn.cursor()

            sql = f"SELECT product_information, name, price, site, furniture_imgs\
                    FROM furniture\
                    INNER JOIN (\
                        SELECT furniture_idx, group_concat(files) as furniture_imgs\
                        FROM furniture_img\
                        WHERE furniture_idx={productIdx}\
                        GROUP BY furniture_idx\
                    ) furniture_img\
                    ON furniture.idx = furniture_img.furniture_idx\
                    WHERE furniture.idx={productIdx}"
            cur.execute(sql)
            result = cur.fetchall()

            self.conn.commit()
            self.disconnect()

            productName = result[0][1]
            productPrice = result[0][2]
            productDescrip = result[0][0]
            productUrl = result[0][3]
            productImgs = str(result[0][4]).split(',')

            getProductRes = GetProductRes(productIdx, productName, productPrice, productDescrip, productUrl, productImgs)

            return getProductRes
        
        except IndexError as e: 
            print(result)
            return BaseResponseStatus.REQUEST_ERROR
        except Exception as e:
            print(e)
            return BaseResponseStatus.UNKNOWN_ERROR
            

        


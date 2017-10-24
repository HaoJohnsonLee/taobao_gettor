#coding=utf-8
import pymysql


connect=pymysql.Connect("*","*","*","*",charset='utf8')


def insert_info(info_price,info_name,info_paynum):
    cursor=connect.cursor()
    sql="insert into nor_info(info_price, info_name, info_paynum) VALUES ('%s','%s','%d')" % \
        (info_price,info_name,info_paynum)
    try:
        cursor.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()
def close():
    connect.close()



#coding=utf-8
import pymysql


#connect=pymysql.Connect("*","*","*","*",charset='utf8')

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

def insert_type(name,href):
    cursor = connect.cursor()
    sql="insert into all_types(type_name, type_href) VALUES ('%s','%s')"%(name,href)
    try:
        cursor.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()

def get_type_id(name):
    cursor = connect.cursor()
    sql="select type_id from all_types WHERE type_name='%s'" % name
    print(sql)
    try:
        cursor.execute(sql)
        return cursor.fetchall()[0][0]
    except Exception as e:
        print(e)
#        0     1    2     3    4     5      6    7   8     9      10
#list0=[书名,作者 出版人 年代 纸张 刻印方式 尺寸 册数 价格 新旧程度 上架时间]
def insert_detail(list0,type):
    cursor = connect.cursor()
    sql="insert into detail(info_name, info_author, info_year, info_page, info_way, info_size, info_num, info_price, info_new, info_sale_time, info_publisher,info_type_id) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d')"%\
    (list0[0],list0[1],list0[3],list0[4],list0[5],list0[6],list0[7],list0[8],list0[9],list0[10],list0[2],type)
    try:
        cursor.execute(sql)
        connect.commit()
    except Exception as e:
        print(e)
        connect.rollback()


def close():
    connect.close()



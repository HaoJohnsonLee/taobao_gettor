# coding=utf-8
import re
import requests
from db import DBhelper


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        paylt = re.findall(r'\"view_sales\"\:\".*?\"', html)
        for i in range(len(plt)):
            try:
                price = eval(plt[i].split(':')[1])
                title = eval(tlt[i].split(':')[1])
                pay = eval(paylt[i].split(':')[1])
                ilt.append([price, title, pay])
            except:
                continue;
    except Exception as e:
        print(e)


def printGoodsList(ilt):
    # tplt = "{:4}\t{:8}\t{:16}\t{:1000}"
    # print(tplt.format("序号", "价格", "商品名称","付款人数"))
    for g in ilt:
        price = g[0]
        name = g[1]
        paynum = g[2][0:-3]
        # print(tplt.format(count, price,name,paynum))
        DBhelper.insert_info(price, name, int(paynum))


def main():
    goods = '二手 图书'
    depth = 100
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    count = 0
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
        count = count + len(infoList)
        printGoodsList(infoList)
        if 0 == (count % 100):
            print(count)
    DBhelper.close()


if __name__ == '__main__':
    main()

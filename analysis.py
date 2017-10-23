#coding=utf-8
import requests
import re
import DBhelper

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
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            pay = eval(paylt[i].split(':')[1])
            ilt.append([price, title,pay])
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}\t{:1000}"
    print(tplt.format("序号", "价格", "商品名称","付款人数"))
    count = 0
    for g in ilt:
        price=g[0]
        name=g[1]
        paynum=g[2][0:-3]
        count = count + 1
        print(tplt.format(count, price,name,paynum))
        DBhelper.insert_info(price, name, paynum)

def main():
    goods = '服装定制'
    depth = 1
    start_url = 'https://s.taobao.com/search?q=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)
    DBhelper.close()
if __name__ == '__main__':
    main()
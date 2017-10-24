import requests
from bs4 import BeautifulSoup
from db import DBhelper as helper

URL = "http://search.kongfz.com/"

"""
   下载该网页 
"""


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content


"""
   获取父子网全部图书类别
        返回字典{类别名:链接} 
"""


def get_all_class(page):
    result = {}
    soup = BeautifulSoup(page, 'html.parser')
    list = soup.find('div', attrs={'class': 'search_list'}).find_all('li')
    for s in list:
        tag = s.a
        result[tag.contents[0]] = tag['href']
    return result


"""
    解析商品列表
     返回list[list0，list1,list2...]
     list0=[书名,作者 出版人 年代 纸张 刻印方式 尺寸 册数 价格 新旧程度 上架时间]
     
     params:
        page:详细列表页面
        type:书籍类型
"""


def get_detail(page,tpye):
    soup = BeautifulSoup(page, 'html.parser')
    result = []
    items = soup.find_all('div', attrs={'class': 'result_box m_t10'})

    for item in items:
        try:
            # 详细信息 包括 作者 书名 册数等
            detail = item.find('div', attrs={'class': 'grid_18 m_r10'})
            name = detail.find('div', attrs={'class': 'result_tit'}).a.string
            info = detail.find('div', attrs={'class': 'info'})
            infos = info.find_all('p')
            info0 = infos[0].string.split("：")[1]  # 作者
            info1 = infos[1].string.split("：")[1]  # 出版人
            info2 = infos[2].string.split("：")[1]  # 年代
            info3 = infos[3].string.split("：")[1]  # 纸张
            info4 = infos[4].string.split("：")[1]  # 刻印方式
            info5 = infos[5].string.split("：")[1]  # 尺寸
            info6 = infos[6].string.split("：")[1]  # 册数
            price = item.find('div', attrs={'class': 'grid_3 txt_right m_r10 font14'})
            price_new = price.find_all('p')
            priceStr = price_new[0].string  # 价格
            new = price_new[1].string  # 新旧程度
            sale_time = item.find('div', attrs={'class': 'grid_3 txt_right m_r10'}).string
            r = [name, info0, info1, info2, info3, info4, info5, info6, priceStr, new, sale_time]
            helper.insert_detail(r, tpye)
            result.append(r)
        except:
            continue
    return result


if __name__ == '__main__':
    # 下载第一个页面
    page = download_page(URL)
    # 获取类型dic
    typesdic = get_all_class(page)
    for key in typesdic:
        print("正在爬取"+key+"的信息")
        basic = typesdic[key]
        type = helper.get_type_id(key)
        for i in range(1, 101):
            print("PAGE:"+str(i))
            #拼接详细页面链接
            href = basic + 'v6w' + str(i)
            page = download_page(href)
            get_detail(page,type)

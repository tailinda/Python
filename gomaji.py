#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 14:39:32 2019

@author: hung-yiwu
"""

# 請連到自己的網路才能開始使用!!!!!!!!!

import pandas as pd
from selenium import webdriver
from time import sleep
import re
import bs4 as BeautifulSoup
from urllib.parse import urljoin
from pandas import ExcelWriter

# 所有 gomaji 網頁的城市 ID 
# Why? 因為懶得進網頁後再抓一次，這個 id 不會很難輸入
cityid = [1, 2, 3, 8, 4, 9, 10 , 11, 12, 5, 6, 13, 14, 15, 16, 17]
cityname = ['大台北', '桃園', '新竹', '苗栗', '台中', '彰化', '南投', '雲林', '嘉義', '台南', '高雄', '屏東', '台東', '花蓮', '宜蘭', '基隆']

# 因為網頁用 js ，所以需要用 selenium 套件，模擬 Google 瀏覽器去把網頁往下拉到底以利我們爬取所有的店家資料
# while 迴圈做的事就是把網頁往下拉
browser = webdriver.Chrome('C:\\Users\\tailinda\\Downloads\\chromedriver.exe')
browser.get('https://www.gomaji.com/ch/7')
sleep(2)
pause_time = 0.5
last_height = browser.execute_script("return document.body.scrollHeight")
while 1:
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(pause_time)
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 將首頁的頁面解析後，爬取所有標籤的網址及標籤名稱
html = browser.page_source
bsObj = BeautifulSoup.BeautifulSoup(html)
tags = bsObj.find_all('li', {'class':'hot-category-list'})
tags_name = []
tags_url = []
for i in range(1, len(tags)):
    tags_name.append(tags[i].text.strip())
    tags_url.append(urljoin('https://www.gomaji.com/', tags[i].find('a', {'href':re.compile('/ch/')}).get('href')))

# 定義一個爬取網頁的函式，後面會以迴圈逐城市逐標籤爬取網頁，到時會經常呼叫到這個函式
# 一樣有 while 迴圈來幫我們把網頁往下拉到底 (js 會自動幫我們顯示更多)
def crawl_gomaji(path):
    global browser
    df = pd.DataFrame(columns = ['縣市', '區域', 'merchant id', '分店 id', '分店名稱', '商品 id', '商品 name', '件數', '商品原價', '商品實際價格'])
    browser.get(path)
    sleep(1)
    pause_time = 0.5
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")
    while 1:
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(pause_time)
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # 分別以 class 去找尋所有的目標值，其中 df 所需要的各種 id ，是從 href 內去切割出來的
    # 因為 id 只會是數字，且那個 href 除了 id 的部分外都沒有用數字，所以可以輕易用正規表達式切割
    html = browser.page_source
    bsObj = BeautifulSoup.BeautifulSoup(html)
    branch_names = bsObj.find_all('h3', {'class':'ellipsis'})
    product_names = bsObj.find_all('h4', {'class':'ellipsis'})
    original_prices = bsObj.find_all('div', {'class':'original line-through'})
    prices = bsObj.find_all('div', {'class':'current'})
    counts = bsObj.find_all('div', {'class':'t-orange t-085 ml-auto'})
    regions = bsObj.find_all('span', {'class':'t-085 t-white'})
    hrefs  = bsObj.find_all('a', {'href':re.compile('/store/')})
    ids = [re.findall('[0-9]+', hrefs[j].get('href')) for j in range(0, len(hrefs))]

    # for_df 是個串列，我們要一列一列地寫入到 df 中，本函式最終直接回傳一個 dataframe
    for k in range(0, len(hrefs)):
        print(k)
        if(len(ids[k]) == 3):
            for_df = [0, regions[k].text, ids[k][0], ids[k][2], branch_names[k].text, ids[k][1], " ".join(product_names[k].text.split()), " ".join(counts[k].text.split()), " ".join(original_prices[k].text.split()), " ".join(prices[k].text.split())]
        else:
            for_df = [0, regions[k].text, ids[k][0], '', branch_names[k].text, ids[k][1], " ".join(product_names[k].text.split()), " ".join(counts[k].text.split()), " ".join(original_prices[k].text.split()), " ".join(prices[k].text.split())]
        df.loc[k] = for_df
    return df

# 巢狀迴圈，最外層是 tag；最內層是 city
# 一個標籤會有 16 個城市，一個城市內的一個標籤就會有一個 df ( 意即就會跑一次 crawl_gomaji )
# 一個的全部城市跑完之後再將每個城市合併起來
# Why? 因為 BD 想要最終格式是 excel 且底下的 sheet 是以標籤去區分
dfs = []
writer = ExcelWriter('C:/Users/tailinda/Desktop/gomaji.xlsx')
for i in range(0, len(tags_url)):
    dfs = []
    for j in range(0, 16):
        path = re.sub('city=1', 'city={}'.format(cityid[j]), tags_url[i])
        df = crawl_gomaji(path)
        df.縣市 = cityname[j]
        dfs.append(df)
    print('爬完 {} 的標籤了！'.format(re.sub('/', '', tags_name[i])))
    table = pd.concat(dfs)
    table.to_excel(writer, '{}'.format(re.sub('/', '', tags_name[i])), index = False)
    worksheet = writer.sheets['{}'.format(re.sub('/', '', tags_name[i]))]
    # 以下的 for 迴圈是在調整 excel 表格的欄位寬度
    for idx, col in enumerate(table):
        series = table[col]
        if(col in ['分店名稱', '商品 name', '縣市', '商品原價', '商品實際價格']):
            k = 2.2
        else:
            k = 1.5
        max_len = max((series.astype(str).map(len).max(),len(str(series.name)))) *k
        worksheet.set_column(idx, idx, max_len)
writer.save()



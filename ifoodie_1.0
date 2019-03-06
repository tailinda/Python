# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 12:09:27 2019

@author: tailinda
"""
#import 套件
import requests as rq
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
from pandas import ExcelWriter
from io import StringIO

# henry1758f
import os 
os.system("pip install openpyxl")
os.system("pip install lxml")
os.system("pip install pandas") 
#

url = "https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/list?page=1"
re = rq.get (url)
soup = BeautifulSoup ( re.text, "lxml" )
encoding = "cp950"


branch_name = []
category = []
avg_price = []
address = []
star = []
review_count = []


gets = soup.find_all("div",{"class":"jsx-1102741263 restaurant-info"})
for get in gets:
    try:
        branch_name.append(get.find("a",{"class":"jsx-1102741263 title-text"}).string.strip()) # henry1758f
    except:
        branch_name.append(np.nan)
    try:
        category.append(get.find_all("a",{"class":"jsx-1102741263 category"}))
        category_result = [category[i][j].text for i in range(0, len(category)) for j in range(1, 3)]
    except:
        category.append(np.nan)
    try:
        avg_price.append(get.find_all("div",{"class":"jsx-1102741263 avg-price"}))
        avg_price_result = [avg_price[i][0].text for i in range(0, len(avg_price))]
    except:
        avg_price.append(np.nan)
    try:
        address.append((get.find("div",{"class":"jsx-1102741263 address-row"}).string).strip())
    except:
        address.append(np.nan)
    try:
        star.append(get.find_all("div",{"class":"jsx-1207467136 text"}))
        star_result = [star[i][0].text for i in range(0, len(star))]
    except:
        star.append(np.nan)
    try:
        review_count.append(get.find_all("a",{"class":"jsx-1102741263 review-count"}))
        review_count_result = [review_count[i][0].text for i in range(0, len(review_count))]
    except:
        review_count.append(np.nan)
        

# 存在表格 CODE
df = pd.DataFrame(columns = ['分店名稱', '類型1', '平均價格', '地址', '星數', '評論數'])
for n in range(0, len(branch_name)):
        df.loc[n] = [branch_name[n], category_result[n], avg_price_result[n], address[n], star_result[n], review_count_result[n]]
# henry1758f
from pathlib import Path
home = str(os.getcwd()+'/test.xlsx')
writer = ExcelWriter(home)
# 

df.to_excel(writer, index=False)
writer.save()

'''
print(branch_name)
print(category_result)
print(avg_price_result)
print(address)
print(star_result)
print(review_count_result)
'''
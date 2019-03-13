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

# 搜尋網頁
url = "https://ifoodie.tw/explore/%E5%8F%B0%E5%8C%97%E5%B8%82/list?page="

#for 迴圈加上頁數
for i in range (1, 3):
    finalurl = url + str(i)

    re = rq.get (finalurl)
    soup = BeautifulSoup ( re.text, "lxml" )
    encoding = "cp950"
    
    branch_name = []
    avg_price = []
    address = []
    star = []
    review_count = []
    avg_price_result = []
    category = []
    category_temp = []
    category_temp_result1 = []
    category_temp_result2 = []
    category_temp_result3 = []
    category_temp_result4 = []
    category_temp_result5 = []
    
    
    gets = soup.find_all("div",{"class":"jsx-1102741263 restaurant-info"})
    for get in gets:
        try:
            branch_name.append(get.find("a",{"class":"jsx-1102741263 title-text"}).string.strip()) # henry1758f
        except:
            branch_name.append("N/A")
        try:
            category_temp = get.find_all("a",{"class":"jsx-1102741263 category"})
            category_temp_result1.append(category_temp[1].text)
        except:
            #加上 N/A
            category_temp_result1.append("N/A")
        try:
            category_temp = get.find_all("a",{"class":"jsx-1102741263 category"})
            category_temp_result2.append(category_temp[2].text)       
        except:
            #加上 N/A
            category_temp_result2.append("N/A")
        try:
            category_temp = get.find_all("a",{"class":"jsx-1102741263 category"})
            category_temp_result3.append(category_temp[3].text)       
        except:
            #加上 N/A
            category_temp_result3.append("N/A")
        try:
            category_temp = get.find_all("a",{"class":"jsx-1102741263 category"})
            category_temp_result4.append(category_temp[4].text)       
        except:
            #加上 N/A
            category_temp_result4.append("N/A")
        try:
            category_temp = get.find_all("a",{"class":"jsx-1102741263 category"})
            category_temp_result5.append(category_temp[5].text)       
        except:
            #加上 N/A
            category_temp_result5.append("N/A")
        try:
            #找到 avg_price 篩選後剩下文字
            rr = get.find("div",{"class":"jsx-1102741263 avg-price"}).text
            #把 rr 放到 avg_price_result 陣列中
            avg_price_result.append(rr)
            """
            else:
                avg_price_result.append("N/A")
                #avg_price.append(get.find_all("div",{"class":"jsx-1102741263 avg-price"}))
                #print(len(avg_price))
                #print(avg_price)
                print(avg_price_result)
            
            if len(get.find_all("div",{"class":"jsx-1102741263 avg-price"})):
                avg_price.append(get.find_all("div",{"class":"jsx-1102741263 avg-price"}))
                print(len(avg_price))
                avg_price_result = [avg_price[i][0].text for i in range(0, len(avg_price))]
                print(avg_price_result)
            else:
                avg_price.append("N/A")
                #avg_price.append(get.find_all("div",{"class":"jsx-1102741263 avg-price"}))
                print(len(avg_price))
                print(avg_price)
                print(avg_price_result)
    
                avg_price_result = [avg_price[i][0].text for i in range(0, len(avg_price))]
                print(avg_price)
                print(avg_price_result)
               """ 
        #例外狀況當作 e
        except Exception as e:
            #加上 N/A
            avg_price_result.append("N/A")
            print(avg_price_result)
    
        try:
            address.append((get.find("div",{"class":"jsx-1102741263 address-row"}).string).strip())
        except:
            address.append("N/A")
        try:
            star.append(get.find_all("div",{"class":"jsx-1207467136 text"}))
            star_result = [star[i][0].text for i in range(0, len(star))]
        except:
            star.append("N/A")
        try:
            review_count.append(get.find_all("a",{"class":"jsx-1102741263 review-count"}))
            review_count_result = [review_count[i][0].text for i in range(0, len(review_count))]
        except:
            review_count.append("N/A")
            
    
    # 存在表格 CODE
    df = pd.DataFrame(columns = ['分店名稱', '類型1', '類型2', '類型3', '類型4', '類型5','平均價格', '地址', '星數', '評論數'])
    for n in range(0, len(branch_name)):
        '''
        print(branch_name)
        print(category_temp_result1)
        print(category_temp_result2)
        print(avg_price_result)
        print(address)
        print(star_result)
        print(review_count_result)
        print(n)
        print(len(branch_name))
        '''
        df.loc[n] = [branch_name[n], category_temp_result1[n], category_temp_result2[n], category_temp_result3[n],
               category_temp_result4[n], category_temp_result5[n],
               avg_price_result[n], address[n], star_result[n], review_count_result[n]]
    
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
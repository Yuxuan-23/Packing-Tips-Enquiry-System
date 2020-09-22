# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 01:28:50 2020

@author: Wangyx
"""

import requests
import json
import urllib
from urllib.parse import quote
from urllib.parse import unquote


# 1-搜索输入时，获取下拉提示
def getSuggest(pre):
    pre = quote(pre)
    url = "https://i.cs.hku.hk/~yxwang2/project/suggest.php?pre=" + pre
    r = requests.get(url)
    data = r.json()
    return (data['name'])



#1-搜索输入时，获取下拉提示   
# pre="tab"
# # print(getSuggest(pre))
# pre="電"
# print(getSuggest(pre))



def searchResults(keyword):
    url = "https://i.cs.hku.hk/~yxwang2/project/fuzzy.php?keyword=" + keyword
    print(url)
    r = requests.get(url)
    data = r.json()
    result = data
    keyword = unquote(keyword)
    for i in range(0, len(data['name'])):
        start = data['name'][i].find(keyword)
        display_len = 30
        if (start != -1):
            if start + display_len >= len(data['name'][i]):
                result['name'][i] = "..." + data['name'][i][start:]
            else:
                result['name'][i] = "..." + data['name'][i][start:start + display_len] + "..."
        else:
            if display_len >= len(data['name'][i]):
                result['name'][i] = data['name'][i]
            else:
                result['name'][i] = data['name'][i][0:display_len] + "..."

    return result


# 2-点击check,根据keyword返回搜索列表
def getCheck(keyword):
    keyword = quote(keyword)
    url = "https://i.cs.hku.hk/~yxwang2/project/search.php?keyword=" + keyword
    r = requests.get(url)
    data = r.json()
    if data['status'] == 'detail':
        # 跳转到行李提示界面
        url = "https://i.cs.hku.hk/~yxwang2/project/detailid.php?cid=" + str(data['cid'])
        r = requests.get(url)
        data = r.json()
        data['detail'] = data['detail'].replace('<br', '\n')
        return "detail", data;

    else:
        # 跳转到搜索结果页面：
        result = searchResults(keyword)
        return "list", result;


# 2-点击check,返回搜索列表
keyword = "swas"
# keyword="電池"
flag, result = getCheck(keyword)
if flag == "detail":
    print("行李提示")
    print('手提行李', result['carry_on'])
    print('寄舱行李', result['checked'])
    print('详情', result['detail'])
else:
    # 跳转到搜索结果页面：
    print("搜索结果：")
    for i in range(0, len(result['category'])):
        print("----------------------------")
        print("第一行：", result['category'][i])
        print("第二行：", result['name'][i])


# 点击搜索列表中的项之后，根据category跳转到详情
def getDetail(category):
    category = quote(category)
    url = "https://i.cs.hku.hk/~yxwang2/project/detail.php?c=" + category
    r = requests.get(url)
    data = r.json()
    data['detail'] = data['detail'].replace('<br', '\n')
    print("行李提示")
    print('手提行李', data['carry_on'])  # 2：-
    print('寄舱行李', data['checked'])
    print('详情', data['detail'])
    return data


# category = "Portable electronic devices containing lithium metal or lithiumion cells or batteries"
category = "內含鋰金屬或鋰離子電池芯或電池的便攜式電子裝置"
getDetail(category)

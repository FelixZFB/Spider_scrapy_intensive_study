# -*- coding:utf-8 -*-

import json

# https://blog.csdn.net/u011318077/article/details/88427872
# json.dump()和json.load()主要用来读写json文件的函数
# json.dump()，将json格式的字符串写入到json文件
# json.load()，将json文件中的内容读取出来，读取结果为字符串

# json.dump()函数的使用，将json信息写进文件
json_info = "{'age': '12'}"
file = open('002.json','w',encoding='utf-8')
json.dump(json_info,file)


# json.load()函数的使用，将读取json信息
file = open('002.json','r',encoding='utf-8')
info = json.load(file)
print(info)
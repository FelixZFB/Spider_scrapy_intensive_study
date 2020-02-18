import json

# json.dumps()函数的使用，将字典类型数据转化为json格式的字符串
dict = {"age": "12"}
json_info = json.dumps(dict)
print("dict的类型："+str(type(dict)))
print("通过json.dumps()函数处理之后：")
print("json_info的类型："+str(type(json_info)))
print("*" * 100)


# json.loads()函数的使用，将json格式的字符串转化为字典
# json_info数据是一个字符串，json数据实际是一个字符串
json_info = '{"age": "12"}'
dict1 = json.loads(json_info)
print("json_info的类型："+str(type(json_info)))
print("通过json.loads()函数处理：")
print("dict1的类型："+str(type(dict1)))
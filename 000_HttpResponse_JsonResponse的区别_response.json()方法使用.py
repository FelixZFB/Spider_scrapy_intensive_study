# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/5/25 22:44
Desc:
'''

# HttpResponse对象
# Django服务器接收到客户端发送过来的请求后，会将提交上来的这些数据封装成一个HttpRequest对象传给视图函数。
# 那么视图函数在处理完相关的逻辑后，也需要返回一个响应给浏览器。
# 而这个响应，我们必须返回HttpResponseBase或者他的子类的对象。
# 而HttpResponse则是HttpResponseBase用得最多的子类。
# 常用属性：
# content：返回的内容。
# status_code：返回的HTTP响应状态码。
# content_type：返回的数据的MIME类型，默认为text/html。

# JsonResponse类：
# 用来对象dump成json字符串，然后返回将json字符串封装成Response对象返回给浏览器。
# 并且他的Content-Type是application/json。
# 返回的是JsonResponse对象，requests获取后直接调用json()方法转变为python字典

# HttpResponse对象
import requests, json
r = requests.get('http://192.168.207.160:9000/api/qualitygates/')
state=json.loads(r.text).get('projectStatus').get('status')

# 请求的内容是json格式数据，先要loads方法反序列化为python的字典格式，然后进行操作
'''
{
 "projectStatus": {
  "status": "ERROR",
  "conditions": [{
   "status": "ERROR",
   "metricKey": "new_security_rating",
   "comparator": "GT",
   "periodIndex": 1,
   "errorThreshold": "1",
   "actualValue": "5"
  }
}
'''

# JsonResponse对象
r = requests.get('http://192.168.207.160:9000/api/qualitygates/')
# 直接调用json方法，返回python下的字典数据
state1 = r.json()
state1.get('projectStatus')



# 字典序列化成json字符串
d = {'name': 'jod'}
j = json.dumps(d)

# json字符串反序列化成字典
d = json.loads(j)
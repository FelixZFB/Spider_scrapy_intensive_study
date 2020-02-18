# requests库，适合人类使用的库 HTTP for Humans
# urllib中使用，request.urlopen,繁琐，不适合人类使用，
# urllib不推荐使用，但是可以通过它可以理解网页请求到返回页面内容整个过程原理

# requests 的底层实现其实就是 urllib

# Requests 继承了urllib的所有特性。Requests支持HTTP连接保持和连接池，
# 支持使用cookie保持会话，支持文件上传，支持自动确定响应内容的编码，支持国际化的 URL 和 POST 数据自动编码。

# 关于编码解码问题
# requests请求网页时候会自动url编码，返回页面内容会自动将字节格式解码为字符串格式
# request.urlopen请求网页时候，带参数或者中文需要先手动URL编码，
# 返回页面内容需要先read读取，然后手动decode解码字节为字符串


#####  urllib的urlopen和Request实例

# urllib库请求返回一个页面步骤：
#     url = 'https://guangdiu.com/detail.php?id=6637916'
#     # 打开一个URL然后返回页面的内容
#     rsp = request.urlopen(url)
#     # 把返回的结果读取出来，直接读取的是字节，默认是Unicode
#     html = rsp.read()
#     print(type(html))
#     # 返回的字节，需要解码，解码以后是字符串,默认是UTF-8
#     content = html.decode()
#     # print(content)
#     print(type(content))

# urllib的下面也有Request实例，先构造一个实例(可以传入url，headers等参数)，然后还是需要urlopen打开：
#       url = 'http://www.baidu.com'
#       headers = {}
#       headers['User-Agent'] = 'Mozilla/5.0 (Linux; U; Android 2.2.1; zh-cn; HTC_Wildfire_A3333 Build/FRG83D)'
#       # 创建请求实例
#       req = request.Request(url, headers=headers)
#       打开实例
#       rsp = request.urlopen(req)
        # 读取解码得到网页内容,读取到的是字节，编码后才是字符串
#       html = rsp.read().decode()




# requests库

# request方法，相对于urllib非常简单，三句代码就可以获取网页内容
# request方法可以接收很多参数，第一个参数是请求网页方式，常用的是get和post
# url = 'http://www.baidu.com'
# rsp = requests.request('get', url)
# # 获取网页内容,字符串格式
# html = rsp.text


# requests使用get方法或者post方法，直接使用方法名替换request即可
# requests库请求返回一个页面步骤：
#     # 字符串拼接，requests.get会自动进行url编码
#     url = "https://www.baidu.com/baidu?wd={}".format("熊猫")
#     # 传入的请求头信息都需要使用字典格式
#     headers = {"User-Agent": "https://www.baidu.com/baidu?tn=monline_3_dg&ie=utf-8&wd=%E7%86%8A%E7%8C%AB"}
#     # 使用get请求，传入网址，请求头
#     response = requests.get(url=url, headers=headers)
#     print(response.text) 打印出来就是字符串格式的页面

#     response.content结果是字节，需要解码为字符串
#     response.content.deocde(“utf-8”)


# 通过对比，实际，requests和urllib本质是相同的，requests就很多方法直接集成到了代码内部，比如read()读取内容
# 爬虫深入研究学习

# requests

# 1 爬虫基本概念补充
## 1.1 字符串知识补充
- bytes：二进制
    - 互联网上的数据都是以二进制的方式传输的
    - 机器编码都是以Unicode
- str
    - Unicode编码的呈现形式
    
- ASCII Unicode UTF-8 之间的关系
    
    字符(Character)是各种文字和符号的总称，包括各国家文字、标点符号、图形符号、数字等
    字符集(Character set)是多个字符的集合
    字符集包括：ASCII字符集、GB2312字符集、GB18030字符集、Unicode字符集等

    ASCII编码是1个字节，而Unicode编码通常是2个字节。
    ASCII 只有127个字符，表示英文字母的大小写、数字和一些符号，但由于其他语言用ASCII 编码表示字节不够，
    例如：常用中文需要两个字节，且不能和ASCII冲突，中国定制了GB2312编码格式，
    相同的，其他国家的语言也有属于自己的编码格式
    
    由于每个国家的语言都有属于自己的编码格式，在多语言编辑文本中会出现乱码，
    这样Unicode应运而生，Unicode就是将这些语言统一到一套编码格式中，通常两个字节表示一个字符，
    而ASCII是一个字节表示一个字符，这样如果你编译的文本是全英文的，
    用Unicode编码比ASCII编码需要多一倍的存储空间，在存储和传输上就十分不划算。
    
    为了解决上述问题，又出现了把Unicode编码转化为“可变长编码”UTF-8编码，
    UTF-8编码将Unicode字符按数字大小编码为1-6个字节，英文字母被编码成一个字节，
    常用汉字被编码成三个字节，如果你编译的文本是纯英文的，
    那么用UTF-8就会非常节省空间，并且ASCII码也是UTF-8的一部分。
  
    UTF-8是Unicode的实现方式之一，它可以看做Unicode的升级版。
    
    计算机系统通用的字符编码工作方式：
    (1) 在计算机内存中，统一使用Unicode编码，当需要保存到硬盘或者需要传输的时候，就转换为UTF-8编码。
    (2) 用记事本编辑的时候，从文件读取的UTF-8字符被转换为Unicode字符到内存里，编辑完成后，保存的时候再把Unicode转换为UTF-8保存到文件

- str和bytes转换
    str 使用encode方法转化为 bytes
    bytes 通过decode转化为str
    编码方式解码方式必须一样，否则就会出现乱码
    python3中默认字符串默认编解码参数是UTF-8

- 参考博客：
    ASCII Unicode UTF-8 之间的关系（简单明了）[https://blog.csdn.net/u011318077/article/details/100086698]
    汉字是两个字节吗？（非也，汉字字节与编码格式有关）[https://blog.csdn.net/u011318077/article/details/88813287]

## 1.2 HTTP和HTTPS
- HTTP
    超文本传输协议 
    默认端口号:80
- HTTPS
    HTTP + SSL(安全套接字层)
    默认端口号：443
- HTTPS比HTTP更安全，但是性能更低
- HTTP常见请求头及含义
    1. Host (主机和端口号)
    2. Connection (链接类型)
    3. Upgrade-Insecure-Requests (升级为HTTPS请求)
    4. User-Agent (浏览器名称)
    5. Accept (传输文件类型)
    6. Referer (页面跳转处)
    7. Accept-Encoding（文件编解码格式）
    8. Cookie （Cookie）
    9. x-requested-with :XMLHttpRequest  (是Ajax 异步请求)
- url的形式(network里面每个请求的url都有详细的信息)
    - 形式   scheme://host[:port#]/path/…/[?query-string][#anchor]
    scheme：协议(例如：http, https, ftp)
    host：服务器的IP地址或者域名
    port：服务器的端口（如果是走协议默认端口，80  or    443）
    path：访问资源的路径
    query-string：参数，发送给http服务器的数据
    anchor：锚（跳转到网页的指定锚点位置）
    http://localhost:4000/file/part01/1.2.html
    http://item.jd.com/11936238.html#product-detail
- markdown插入代码
```python
import json
print('hello world')
```
- 访问网络的两种方法
    - get 
        - 利用参数给服务器传递信息
        - 参数为dict,使用parse编码
        - 看实例43_4
    - post
        - 一般向服务器传递参数使用
        - post是把信息自动加密处理
        - 我们如果想使用post信息，需要使用data参数
        - 使用post,意味着http请求头可能需要更改:
            - Content-Type: application/x-www.form-urlencode
            - Content-Length: 数据长度
            - 简而言之，一旦更改请求方法，注意其它请求头部信息相适应         
            - 看实例43_5/6
            - 为了更多的设置请求信息，单纯通过urlopen就不太适用了
            - 需要使用request.Request类 

- get与post请求的区别：
    POST请求的参数都在放在formdata中，可以查看有道翻译，翻译一个单词，
    检查network中headers，里面有formdata，里面有发送请求的相关参数。
    浏览器地址栏中的网址没有发生变化。
    
    get请求：请求的参数直接放在url地址之中，
    请求的参数进行url编码直接放在地址中
            
    - POST请求一般用于提交表单，传输大量的数据
    - 其它请求一般都使用的GET请求
    - POST不同的请求网址不变，GET不同的请求网址发生变化
    
- 搜索引擎及ROBOTS协议
    - 排名规则：pagerank算法，点击次数，被引用次数
    - 局限性：
        通用搜索引擎所返回的网页里90%的内容无用
        图片，音频，视频多媒体内容通用搜索引擎无能为力
        不同用户搜索的目的不全相同，但是返回的内容相同
    - ROBOTS协议：网站自己定义的允许和不允许的一些规则
    - 告诉搜索引擎哪些网页可以抓取，哪些页面不能抓取
    - 但是只是网站自己的规定，道德层面的约定，只要能打开相应网页，还是可以爬取
    - https://www.taobao.com/robots.txt
        User-agent:  Baiduspider
        Allow:  /article
        Allow:  /oshtml
        Allow:  /ershou
        Allow: /$
        Disallow:  /product/
        Disallow:  /
        
        User-Agent:  Googlebot
        Allow:  /article
        Allow:  /oshtml
        Allow:  /product
        Allow:  /spu
        Allow:  /dianpu
        Allow:  /oversea
        Allow:  /list
        Allow:  /ershou
        Allow: /$
        Disallow:  /
    
## 1.3 爬虫概念
- 爬虫要根据当前的URL地址对应的响应为准
    Chrome或者Firefox里面的network查看，浏览器一个网址请求network会出来很多请求
    elements的内容和URL地址的响应不一样，network中的第一个请求才是当前的URL地址请求
- 浏览器页面上的数据在哪里
    当前url地址对应的响应中
    其它的url地址对应的响应中
        - 比如ajax请求中
    .js生成的
        - 部分数据在响应中
        - 全部通过js生成
       
# 2. requests库
## 2.1 response.text 和response.content的区别
- 1.response.text
    - 类型：str
    - 解码类型： 根据HTTP 头部对响应的编码作出有根据的推测，推测的文本编码
    - 如何修改编码方式：response.encoding=”gbk”
- 2. response.content
    - 类型：bytes
    - 解码类型： 没有指定
    - 如何修改编码方式：response.content.deocde(“utf-8”)
- 3. 区别
    使用response.text 时，Requests 会基于 HTTP 响应的文本编码自动解码响应内容，大多数 Unicode 字符集都能被无缝地解码。
    使用response.content 时，返回的是服务器响应数据的原始二进制字节流，可以用来保存图片等二进制文件。
    requests默认自带的Accept-Encoding导致或者网站默认发送的就是压缩之后的网页
    但是为什么content.read()没有问题，因为requests，自带解压压缩网页的功能
    当收到一个响应时，Requests会猜测响应的编码方式，用于在你调用response.text方法时对响应进行解码。
    Requests首先在HTTP头部检测是否存在指定的编码方式，如果不存在，则会使用chardet.detect来尝试猜测编码方式（存在误差）
    更推荐使用response.content.deocde()
- 4.获取网页源码的通用方式：
    response.content.decode()
    response.content.decode(“GBK”)
    解码方式可以根据响应头中找到Content-Type:text/html;charset=utf-8或者网页源码中content="text/html;charset=utf-8’'来决定.
    response.encoding = "utf-8"
    response.text
    以上三种方法从前往后尝试，能够100%的解决所有网页解码的问题
    所以：更推荐使用**response.content.decode()**的方式获取响应的html页面

# 3. 使用代理IP和代理UserAgent
- 准备一堆的ip地址，组成ip池，随机选择一个ip来使用
- 如何选择随机代理ip,让使用次数最少的ip被用到
    - {"ip":ip, "times": 0}
    - 对这个ip列表进行排序，按照使用次数进行排序，[{}, {}, {}],sorted排序方法
    - 选择使用次数最少的IP，从中在随机选择一个
- 检查ip的可用性
    - 可以使用requests添加超时参数timeout=3，判断ip的质量
    - 也可以使用在线ip质量检测网站
- 参考TZKT_Study_Note中006案例，西刺代理爬取及使用，使用随机代理UserAgent
    
# 4. cookie和session区别
- 区别
    cookie数据存放在客户的浏览器上，session数据放在服务器上。
    cookie不是很安全，别人可以分析存放在本地的cookie并进行cookie欺骗。
    session会在一定时间内保存在服务器上。当访问增多，会比较占用你服务器的性能。
    单个cookie保存的数据不能超过4K，很多浏览器都限制一个站点最多保存20个cookie。

- 爬虫处理cookie和session
    带上cookie、session的好处：
	- 能够请求到登录之后的页面
    - 带上cookie、session的弊端：
        一套cookie和session往往和一个用户对应
        请求太快，请求次数太多，容易被服务器识别为爬虫
    - 不需要cookie的时候尽量不去使用cookie
    - 但是为了获取登录之后的页面，我们必须发送带有cookies的请求

- urllib和http库处理cookie：
        from urllib import request, parse
        from http import cookiejar
        cookiejar模块可以自动提取已经登录后产生的cookie
        - 参考Spider_development_study_note中001文件夹中相关案例

- requests库处理cookies 、session请求
    requests 提供了一个叫做session类，来实现客户端和服务端的会话保持
    使用方法：
        - 实例化一个session对象
            session = requests.session()
        - 使用session发送请求，登录网址，会自动把cookie保存到session中
            response = session.get(url,headers)
        - 再使用session请求登录之后才能访问的网址，session能够自动使用登录成功时保存的cookie，进行请求
    - 参考001文件夹中008案例
    
- cookie信息直接登陆有两种方式
    获取到cookie后可以直接放在headers字典里面，直接使用
    cookie信息放在get参数的cookies中
    - 参考001文件夹中009/010案例
       
- 不发送post请求，直接本地的cookie信息登陆的情况：
    - cookie信息过期时间很长的网址
    - cookie信息过期前，我们可以获取我们所需要的数据
    - 配合一些其它程序使用，其它程序专门获取cookie，当前程序专门用来请求页面
    
# 5. POST请求地址
- 在form表单中寻找action对应的url地址
    - post的数据是input标签中name的值作为键，真正的用户名和密码作为值
    - post的url地址就是action对应的url地址
    - 参考001文件中008图片

- 抓包，寻找登陆的url地址
    - Chrome的network下勾选上preserve log按钮，不会清楚跳转之前的页面
    - 多次尝试输入用户名和错误的密码，寻找请求的规律
        - 寻找post数据，确定参数
            - 参数不变直接使用，比如密码不是动态加密
            - 参数会变  - 参数在当前的响应中，通过js生成
    
- 定位想要的js
    - 选择会触发js时间的按钮，点击event listener，找到js的位置
    - 通过Chrome中检查元素，最右侧的search all file寻找url中的关键字
    - 添加断点的方式来查看js的操作
    
# 6. requests使用小技巧
- 010案例中我们使用的字典生成式转换原始cookies
- 实际可以直接使用cookies转换工具
- 参考案例011

- requests使用小技巧
    1、requests.utils.dict_from_cookiejar(cookies)  把cookie对象转化为字典
        cookies转换为字典后，就可以加入到get的参数中使用
        1.1. requests.get(url,cookies={})
    
    2、请求SSL证书验证，添加一个参数，跳过证书验证
       response = requests.get("https://www.12306.cn/mormhweb/ ", verify=False)
    
    3、设置超时,有些网址网速不好，设置一个超时参数，超过了就直接结束请求
       response = requests.get(url,timeout=3)
    
    4、配合状态码判断是否请求成功
       assert response.status_code == 200
    
    5、retrying重试功能
        
- 使用技巧参考001文件夹中案例012   

  
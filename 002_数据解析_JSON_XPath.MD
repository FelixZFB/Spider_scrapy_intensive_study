# 数据解析

# 1. json
- 由于把json数据转化为python内建数据类型很简单，所以爬虫中，如果我们能够找到返回json数据的URL，就会尽量使用这种URL
- JSON(JavaScript Object Notation) 是一种轻量级的数据交换格式，它使得人们很容易的进行阅读和编写。
- 同时也方便了机器进行解析和生成。适用于进行数据交互的场景，比如网站前台与后台之间的数据交互。

- 那么问题来了：哪里能找到返回json的url呢？
    web返回的都是html页面，但是手机页面，响应内容可能是json格式内容
	1、使用chrome切换到手机页面
	2、抓包手机app的软件
	
- json文件处理的四个函数json.dumps()、json.loads()、json.dump()和json.load()的区分
    (1)json.dumps()函数：是将一个Python数据类型列表，进行json格式的编码
    （可以这么理解，json.dumps()函数是将字典转化为字符串）
    (2)json.loads()函数：是将json格式数据转换为字典
    （可以这么理解，json.loads()函数是将字符串转化为字典）
    (3)json.dump()和json.load()主要用来读写json文件的函数 
    json.dump()，将json格式的字符串写入到json文件
    json.load()，将json文件中的内容读取出来，类似字典格式读取出来就是字典，如果是数组形式，读取出来就是列表
    - 具体区别参考Python_development_skills_summary中的004文件夹
    
# 2. XPath
- 详细使用参考：Python_advanced_learning项目中XPath相关知识

- 常用扩展工具
    - Firefox 
        XpathFinder 鼠标放在元素上，就可以显示出XPath路径
        TryXpath 验证你的XPath表达式是否正确
    - Chrome 
        XpathHelper 显示XPath路径和验证手写的XPath路径是否正确

- Xpath重点，常用查找
- 获取文本
    - a/text() 获取a标签下的文本
    - //text() 获取a标签下的所有文本
    - //a[text()="下一页"] 选择文本为“下一页”三个字的a标签
    - //a[text()="下一页"]/@href 选择文本为“下一页”三个字的a标签href属性的值，即下一页的url地址

- @符号
    - 选取属性
    - a/@href 获取a标签下href的属性的值
    - //ul[@id="detail-list"] 获取所有id属性为detail-list的ul标签

- /
    - 逐级向下提取
    - /html/body/div/li
    - /html/body/div[2]/li[3]
    - 当每一级只有一个相同标签，逐级向下提取
    - 如果每一级有多个相同标签，可以采用类似列表提取元素的方式


- //
    - // 在xpath开始的时候从当前html中任意位置开始选择
    - li//a 获取li标签下的所有a标签
    
- . 选择当前节点，当前选择的是html节点，./body/div即代表从html节点开始选择body
  .. 选取当前节点的父节点
  
- Python中使用Xpath
    # 1 导入模块
    import requests
    from lxml import etree
    # 2 获取文本，r.text类型是字符串文本内容，
        如果使用r.content则是bytes字节，还需要解码r.content.decode()
        解码会自动推测编码格式
    r = requests.get(url, headers=headers)
    text = r.text
    # 3 text解析为xml格式，就可以使用xpath查找了
    html = etree.HTML(text,etree.HTMLParser())
    # 4 查找标签，返回值是列表
    jobs = html.xpath(".//div[@id='resultList']//div[@class='el']")
    
- 也可以使用parsel的Selector(用法和scrapy中一样)
    - from parsel import Selector
    - html = Selector(response.text)    生成一个选择器对象，类似于上面的etree解析
    - title = html.xpath("xxx").extract_first()
    
    - scrapy中初始网址的响应直接使用response.xpath()即可
    - response查找结果，比如li标签继续查找，也是直接li.xpath()

- Xpath使用注意点：
- 上面html = etree.HTML(text,etree.HTMLParser())返回值是一个Element对象
    - 如果要查看里面的经过处理后的html代码字符串内容，可以使用以下方法:
    - etree.tostring(html).decode()
    - etree.HTML方法会对原始html字符串自动校准修改，有时候会出现和源码不同的情况
    - 可以使用上面方法打印出来进行对比
- etree.HTML可以接收bytes和str数据

        
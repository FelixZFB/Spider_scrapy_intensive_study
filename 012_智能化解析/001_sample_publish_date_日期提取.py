# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/9/9 16:52
Desc:
'''

import re
from lxml.html import HtmlElement, fromstring

# 将 html 里面的字符转化成 lxml 里面的 HtmlElement 对象
# element 对象其实就是整个网页对应的 HtmlElement 对象，其根节点就是 html
html = open('sample.html', encoding='utf-8').read()
element = fromstring(html=html)

# 日期时间提取：
# 第一步：meta 提取

# 匹配发布时间的 XPath 规则
METAS = [
    '//meta[starts-with(@property, "rnews:datePublished")]/@content',
    '//meta[starts-with(@property, "article:published_time")]/@content',
    '//meta[starts-with(@property, "og:published_time")]/@content',
    '//meta[starts-with(@property, "og:release_date")]/@content',
    '//meta[starts-with(@itemprop, "datePublished")]/@content',
    '//meta[starts-with(@itemprop, "dateUpdate")]/@content',
    '//meta[starts-with(@name, "OriginalPublicationDate")]/@content',
    '//meta[starts-with(@name, "article_date_original")]/@content',
    '//meta[starts-with(@name, "og:time")]/@content',
    '//meta[starts-with(@name, "apub:time")]/@content',
    '//meta[starts-with(@name, "publication_date")]/@content',
    '//meta[starts-with(@name, "sailthru.date")]/@content',
    '//meta[starts-with(@name, "PublishDate")]/@content',
    '//meta[starts-with(@name, "publishdate")]/@content',
    '//meta[starts-with(@name, "PubDate")]/@content',
    '//meta[starts-with(@name, "pubtime")]/@content',
    '//meta[starts-with(@name, "_pubtime")]/@content',
    '//meta[starts-with(@name, "weibo: article:create_at")]/@content',
    '//meta[starts-with(@pubdate, "pubdate")]/@content',
]

# 提取时间，方法里面表明了对象是HtmlElement，类型是str，是为了方便理解代码
# 对 METAS 进行逐个遍历，然后查找整个 HtmlElement 里面是不是有匹配的内容
# //meta[starts-with(@property, "og:published_time")]/@content
# 这个就是查找 meta 节点中是不是存在以 og:published_time 开头的 property 属性，如果存在，那就提取出其中的 content 属性内容。
def extract_by_meta(element: HtmlElement) -> str:
    for xpath in METAS:
        # 网页 html 对象依次传入不同的xpath规则进行匹配，匹配到结果，结果里面是一个列表，拼接里面空格都没有，就是返回content 内容的字符串
        datetime = element.xpath(xpath)
        # ['2019-02-20 02:26:00']
        if datetime:
            return ''.join(datetime)
print(extract_by_meta(element))


# 方式2：正则提取时间日期
# 并不是所有的页面都会包含这个 meta 标签，如果不包含的话，我们还需要进行第二步的提取
# 一些常用的时间正则表达式来进行提取的方法
REGEXES = [
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
    "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
    "(\d{4}年\d{1,2}月\d{1,2}日)",
    "(\d{2}年\d{1,2}月\d{1,2}日)",
    "(\d{1,2}月\d{1,2}日)"
]


# 将 html 文档的所有文字内容拼接为一个整体，然后使用正则表达式搜索
def extract_by_regex(element: HtmlElement) -> str:
    text = ''.join(element.xpath('.//text()'))
    # print(text)
    for regex in REGEXES:
        result = re.search(regex, text)
        if result:
            return result.group(1)

print(extract_by_regex(element))

# 通过上面两种方式一般都可以准确提取出时间日期

# 最后我们将提取方法定义为下面方法，先使用meta方法提取，然后再使用正则
def extract_publish_date(element):
    return extract_by_meta(element) or extract_by_regex(element)

print(extract_publish_date(element))
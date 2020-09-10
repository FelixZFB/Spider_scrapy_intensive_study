# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/9/10 11:26
Desc:
'''

import re
from lxml.html import HtmlElement, fromstring

# 将 html 里面的字符转化成 lxml 里面的 HtmlElement 对象
# element 对象其实就是整个网页对应的 HtmlElement 对象，其根节点就是 html
html = open('sample.html', encoding='utf-8').read()
element = fromstring(html=html)


# 第一步：使用meta标签进行匹配
# 这个就是查找 meta 节点中是不是存在以 og:title 开头的 property 属性，如果存在，那就提取出其中的 content 属性内容。
METAS = [
    '//meta[starts-with(@property, "og:title")]/@content',
    '//meta[starts-with(@name, "og:title")]/@content',
    '//meta[starts-with(@property, "title")]/@content',
    '//meta[starts-with(@name, "title")]/@content',
    '//meta[starts-with(@property, "page:title")]/@content',
]

def extract_by_meta(element: HtmlElement) -> str:
    for xpath in METAS:
        title = element.xpath(xpath)
        if title:
            # 上面的结果是列表，列表中元素返回为字符串
            return ''.join(title).strip()
print(extract_by_meta(element))


# 提取 title 和 h1~h3 节点的信息，去除空格
def extract_by_title(element: HtmlElement):
    return ''.join(element.xpath('//title//text()')).strip()
print(extract_by_title(element))

def extract_by_h(element: HtmlElement):
    return ''.join(
        element.xpath('(//h1//text() | //h2//text() | //h3//text())')).strip()
print(extract_by_h(element))


# meta如果匹配到，一般结果很准确
# title或者h节点 包含一些冗余信息，仔细想想确实是这样的，因为 title 一般来说会再加上网站的名称，而 h 节点众多，通常会包含很多噪音
# 公共连续内容其实就好了，这里用到一个算法，就是最长连续公共子串，即 Longest Common String，这里我们直接借助于 Python 的 difflib 库来实现即可
from difflib import SequenceMatcher
def lcs(a, b):
    match = SequenceMatcher(None, a, b).find_longest_match(0, len(a), 0, len(b))
    return a[match[0]: match[0] + match[2]]
# 定义了一个 lcs 方法，它接收两个字符串类型的参数，比如 abcd 和 bcde，那么它的返回结果就是它们的公共部分，即 bcd

def extract_title(element: HtmlElement):
    title_extracted_by_meta = extract_by_meta(element)
    title_extracted_by_h = extract_by_h(element)
    title_extracted_by_title = extract_by_title(element)
    # meta 存在匹配直接返回
    if title_extracted_by_meta:
        return title_extracted_by_meta
    # title 和 h 都存在，取公共最长连续字符串
    if title_extracted_by_title and title_extracted_by_h:
        return lcs(title_extracted_by_title, title_extracted_by_h)
    # title，存在，取title
    if title_extracted_by_title:
        return title_extracted_by_title
    # 只存在 h，只能取h了
    return title_extracted_by_h



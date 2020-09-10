# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
WeiXin: AXiaShuBai
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
GihHub: https://github.com/FelixZFB
Date: 2020/9/10 17:05
Desc:
'''

# 第一步：
# 正文的提取需要我们做一些预处理工作，比如一个 html 标签内有很多噪音，非常影响正文的提取，
# 比如说 script、style 这些内容，一定不会包含正文，但是它们会严重影响文本密度的计算，所以这里我们先定义一个预处理操作

from lxml.html import HtmlElement, etree

# CONTENT_USELESS_TAGS 代表一些噪音节点，可以直接调用 strip_elements 把整个节点和它的内容删除。
CONTENT_USELESS_TAGS = ['meta', 'style', 'script', 'link', 'video', 'audio', 'iframe', 'source', 'svg', 'path',
                        'symbol', 'img']
# CONTENT_STRIP_TAGS ，这些节点文本内容需要保留，但是它的标签是可以删掉的
CONTENT_STRIP_TAGS = ['span', 'blockquote']
# CONTENT_NOISE_XPATHS，这是一些很明显不是正文的节点，如评论、广告等，直接移除就好
CONTENT_NOISE_XPATHS = [
    '//div[contains(@class, "comment")]',
    '//div[contains(@class, "advertisement")]',
    '//div[contains(@class, "advert")]',
    '//div[contains(@style, "display: none")]',
]


def preprocess4content(element: HtmlElement):
    # remove tag and its content
    etree.strip_elements(element, *CONTENT_USELESS_TAGS)
    # only move tag pair
    etree.strip_tags(element, *CONTENT_STRIP_TAGS)
    # remove noise tags
    remove_children(element, CONTENT_NOISE_XPATHS)

    for child in children(element):

        # merge text in span or strong to parent p tag
        if child.tag.lower() == 'p':
            etree.strip_tags(child, 'span')
            etree.strip_tags(child, 'strong')

            if not (child.text and child.text.strip()):
                remove_element(child)

        # if a div tag does not contain any sub node, it could be converted to p node.
        if child.tag.lower() == 'div' and not child.getchildren():
            child.tag = 'p'

#
def remove_element(element: HtmlElement):
    parent = element.getparent()
    if parent is not None:
        parent.remove(element)
def remove_children(element: HtmlElement, xpaths=None):
    if not xpaths:
        return
    for xpath in xpaths:
        nodes = element.xpath(xpath)
        for node in nodes:
            remove_element(node)
    return element
def children(element: HtmlElement):
    yield element
    for child_element in element:
        if isinstance(child_element, HtmlElement):
            yield from children(child_element)


# 第二步：
# 预处理完毕之后，整个 element 就比较规整了，去除了很多噪声和干扰数据。
# 实现文本密度和符号密度的计算吧。为了方便处理，这里我把节点定义成了一个 Python Object，
# 名字叫作 ElementInfo，它里面有很多字段，代表了某一个节点的信息，比如文本密度、符号密度等
from lxml.html import HtmlElement
from pydantic import BaseModel

class ElementInfo(BaseModel):
    id: int = None
    tag_name: str = None
    element: HtmlElement = None
    number_of_char: int = 0
    number_of_linked_char: int = 0
    number_of_tag: int = 0
    number_of_linked_tag: int = 0
    number_of_p_tag: int = 0
    number_of_punctuation: int = 0
    density_of_punctuation: int = 1
    density_of_text: int = 0
    density_score: int = 0

    class Config:
        arbitrary_types_allowed = True


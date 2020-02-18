# -*- coding:utf-8 -*-
# project_xxx\venv\Scripts python

'''
Author: Felix
Email: xiashubai@gmail.com
Blog: https://blog.csdn.net/u011318077
Date:  21:03
Desc:
'''

import json
import re
import requests

def json_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
    }
    response = requests.get(url, headers=headers, timeout=3)
    js_info = response.content.decode() # 返回内容还是一个json格式的字符串

    # json格式字符中查找内容,查找aid对应的值即视频的编号
    # ret = re.findall(r'''"aid":(\d+),''', js_info)
    # ret = sorted(set(ret), key=ret.index) # 去除相同的元素并按与按原顺序排列

    # 可以打开查看原始url,每个视频都是放在archives对应的值中，一个列表中
    html = json.loads(js_info)  # 转换为python支持的字典格式
    video_list = html["data"]["archives"]

    # 提取每个视频需要的信息，最后汇总到一个列表中
    all_videos = list()
    for video in video_list:
        video_info = dict()
        # 提取视频标题，url地址，作者，观看次数，喜欢次数
        video_info['title'] = video["title"]
        video_info['url'] = "https://www.bilibili.com/video/av{}/".format(str(video["aid"]))
        video_info['author'] = video["owner"]["name"]
        video_info['view'] = video["stat"]["view"]
        video_info['like'] = video["stat"]["like"]
        # 存储视频信息
        with open("016_all_videos.txt", "a", encoding="utf-8") as f:
            f.write(str(video_info) + "\n")

        all_videos.append(video_info)


if __name__ == '__main__':
    # 真实请求的url地址是通过js分析得到的，具体步骤参考004_JS动态请求页面分析.MD中详细过程
    # 网址也可以通过下一页获取，此处我们直接构造url列表
    for i in range(0, 10):
        url = "https://api.bilibili.com/x/web-interface/newlist?&rid=22&type=0&pn={}&ps=20".format(i)
        # 请求每一个url
        print(url)
        json_request(url)

# url的rid即视频栏目，pn即栏目下的视频页码，通过修改这两个参数就可以爬取所有的视频信息
# 没有cookie登陆，模拟登陆人人网
# 先登陆自己人人网个人主页，复制主页的网址，
# 如果关闭浏览器后再次打开浏览器，粘贴网址，由于浏览器保存了cookie信息，会进入到个人主页
# 个人主页地址复制到另外一台电脑登陆或者另外一个浏览器，由于没有cookie登陆会跳转到人人网主页

import chardet
from urllib import request

if __name__ == '__main__':

    # 个人人人网登陆后的个人主页
    url = 'http://www.renren.com/574862780'
    rsp = request.urlopen(url)
    html = rsp.read().decode('UTF-8')
    # 将打开的网页保存为html文件，然后浏览器打开，打开后是人人网主页
    with open('43_11_rsp.html', 'w') as f:
        f.write(html)




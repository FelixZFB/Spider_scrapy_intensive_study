# 使用cookie登陆，模拟登陆人人网
# 先登陆自己人人网个人主页，复制主页的网址，
# 如果关闭浏览器后再次打开浏览器，粘贴网址，由于浏览器保存了cookie信息，会进入到个人主页
# 个人主页地址复制到另外一台电脑登陆或者另外一个浏览器，由于没有cookie登陆会跳转到人人网主页
# 复制已登录的主页中的cookie信息到请求头中
# 注意cookie有时效性，第二天再次使用可能cookie已经失效

import chardet
from urllib import request

if __name__ == '__main__':

    # 个人人人网登陆后的个人主页
    url = 'http://www.renren.com/969464538/profile'
    headers = {'Cookie': 'anonymid=jqz93aa61j2ebq; depovince=ZGQT; _r01_=1; JSESSIONID=abcCDVfle7EH5eGmyXAHw; ick_login=2c2236f7-9001-4b87-8f7a-4d1ef7936834; t=0c73459378e50f6e3ee47ae345e53ff28; societyguester=0c73459378e50f6e3ee47ae345e53ff28; id=969464538; xnsid=a53a566e; jebecookies=f50fc9af-aab9-4b0e-ba46-2f6662e91791|||||; ver=7.0; loginfrom=null; wp_fold=0'}
    req = request.Request(url, headers=headers)
    rsp = request.urlopen(req)
    html = rsp.read().decode()
    # 将打开的网页保存为html文件，然后浏览器打开
    with open('43_12_rsp.html', 'w') as f:
        f.write(html)




# 自动使用cookie登陆的流程
# 打开登陆页面后自动通过用户密码登陆
# 自动提取反馈回来的cookie
# 利用提取的cookie登陆隐私页面

from urllib import request, parse
from http import cookiejar

# 创建cookiejar的实例
cookie = cookiejar.CookieJar()
# 生成cookie的管理器
cookie_handler = request.HTTPCookieProcessor(cookie)
# 创建http请求管理器
http_handler = request.HTTPHandler()
# 生成https管理器
https_handler = request.HTTPSHandler()
# 创建请求管理器
opener = request.build_opener(http_handler, https_handler, cookie_handler)

# 初次登录,验证后给我们cookie
def login():
    '''
    负责初次登录
    需输入用户名和密码，用来获取cookie凭证
    '''
    # 登录用户地址，进入人人网登录首页，查看网页源码
    # 网页源码中打开查找，查找“下次自动登录”
    # 然后向上找form，里面就有提交表单的地址格式，login-form
    url = 'http://www.renren.com/PLogin.do'

    # 此键值需要从登录form的对应两个input中提取name属性
    data = {'email': '908851835@qq.com', 'password': 'zfb123456zfb'}

    # 把数据进行编码
    data = parse.urlencode(data)

    # 创建一个请求对象
    req = request.Request(url, data=data.encode())

    # 使用opener发起请求,会自动提取我的cookie
    rsp = opener.open(req)

def getHomePage():
    url = 'http://www.renren.com/574862780'

    # 如果已经执行了login,则opener则自动已经包含了相应的cookie值
    rsp = opener.open(url)
    # 读取网页的内容并进行解码
    html = rsp.read().decode()
    # 将打开的网页保存为html文件，然后浏览器打开
    with open('43_13_rsp.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    # 初次使用用户名密码登陆后提取得到cookie
    login()
    # 使用获取的额cookie登陆个人主页
    getHomePage()



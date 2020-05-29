
# 1 Pyppeteer 介绍
- Selenium 存在问题：
    - 很多时候我们会发现 Selenium 有一些不太方便的地方，比如环境的配置，
    - 得安装好相关浏览器，比如 Chrome、Firefox 等等，然后还要到官方网站去下载对应的驱动，
    - 最重要的还需要安装对应的 Python Selenium 库，而且版本也得好好看看是否对应，确实不是很方便，
    - 另外如果要做大规模部署的话，环境配置的一些问题也是个头疼的事情。

- Puppeteer 介绍：   
    - Puppeteer 是 Google 基于 Node.js 开发的一个工具，
    - 有了它我们可以通过 JavaScript 来控制 Chrome 浏览器的一些操作
    - 当然也可以用作网络爬虫上，其 API 极其完善，功能非常强大

- Pyppeteer 又是什么呢？
    - 它实际上是 Puppeteer 的 Python 版本的实现，但它不是 Google 开发的，
    - 是一位来自于日本的工程师依据 Puppeteer 的一些功能开发出来的非官方版本。
    - Pyppeteer 就是依赖于 Chromium 这个浏览器来运行的。
    - 那么有了 Pyppeteer 之后，我们就可以免去那些烦琐的环境配置等问题。
    - 如果第一次运行的时候，Chromium 浏览器没有安装，那么程序会帮我们自动安装和配置，就免去了烦琐的环境配置等工作。
    - 另外 Pyppeteer 是基于 Python 的新特性 async 实现的，所以它的一些执行也支持异步操作，效率相对于 Selenium 来说也提高了。
    - windows: pip install pyppeteer
    - Linux: pip3 install pyppeteer 

# 2 Pyppeteer 入门使用
- 爬取网页：https://dynamic2.scrape.cuiqingcai.com/
- 页面分析：
    - 整个页面是用 JavaScript 渲染出来的，同时一些 Ajax 接口还带有加密参数，
    - 所以这个网站的页面我们无法直接使用 requests 来抓取看到的数据，网页源码只有一些css和js文件引用代码
    - 由于Ajax请求地址带有加密参数，无法准确获取真实的Ajax请求地址，就不太好直接模拟 Ajax 请求来获取真实的数据
    - 无法获取Ajax动态请求的真实接口，加密数据随时变化，无法找出准确规律
    - 这种网页只能通过浏览器渲染出来后，从渲染页面获取数据


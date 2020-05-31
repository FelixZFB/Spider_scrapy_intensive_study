# Pyppeteer 使用教程

# [Pyppeteer官方文档](https://miyakogi.github.io/pyppeteer/reference.html)

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
    
    - Pyppeteer 安装：
    - windows: pip install pyppeteer
    - Linux: pip3 install pyppeteer 
    - 第一次运行时候，会自动安装chromium,但是由于网络问题会出错，直接网上下载后安装
    - 具体步骤：
        - 下载 chromium 浏览器到本地，百度搜索下载一个即可，然后解压
        - 查看 pyppeteer 判断 chromium 浏览器是否需要下载的本地路径，参考下图，先找到虚拟环境下chromium_downloader.py文件，然后代码中添加方框中两句代码，然后运行，就可以打印出本地浏览器路径
        - 接着进入路径local-chromium文件夹下，创建一个588429文件夹，然后将 chromium 浏览器文件夹复制进去即可
        - 再次运行代码，会自动从该路径中下载 chromium 浏览器，然后自动配置，配置完成后里面会多一个chrom-win32文件夹，推测就是将我们复制进去的chromium 浏览器下载复制了一遍
        - 查看003/004图片
        - 参考个人博文：https://blog.csdn.net/u011318077/article/details/106453697 


# 2 Pyppeteer 入门使用
- 爬取网页：https://dynamic2.scrape.cuiqingcai.com/
- 页面分析：
    - 整个页面是用 JavaScript 渲染出来的，同时一些 Ajax 接口还带有加密参数，
    - 所以这个网站的页面我们无法直接使用 requests 来抓取看到的数据，网页源码只有一些css和js文件引用代码
    - 由于Ajax请求地址带有加密参数，无法准确获取真实的Ajax请求地址，就不太好直接模拟 Ajax 请求来获取真实的数据
    - 无法获取Ajax动态请求的真实接口，加密数据随时变化，无法找出准确规律
    - 这种网页只能通过浏览器渲染出来后，从渲染页面获取数据
- 具体查看文件夹010中001案例

- Pyppeteer 对比 Selenium 的优势
- 优势1：
    - 支持异步操作
    - 案例中可以看出，Pyppeteer使用方法类似于Selenium,第一步也是创建浏览器对象，
    - 但是多一步创建浏览器页面然后之后一样，可以对比查看004文件夹中006案例
    - 都是先请求页面，获取动态渲染后的页面源码，然后提取数据，最后关闭浏览器对象
    - 但是Pyppeteer支持async异步协程操作，因此爬取效率更高

- 优势2：
    - 配置简单
    - Pyppeteer配置 Chrome 浏览器，也没有配置浏览器驱动，免去了一些烦琐的步骤，
    - 同样达到了 Selenium 的效果，还实现了异步抓取。

- 优势3：
    - 数据提取简洁
    - Pyppeteer 源码直接解析为pyquery对象，然后css解析
    - Selenium需要使用自己的语法，写法更复杂一点，比如：
        - find_element_by_id
        - find_element_by_xpath

# 3 Page 页面
- Page 即页面，就对应一个网页，一个选项卡。
- 001/002/005案例中已经演示了几个 Page 方法的操作了，这里我们再详细看下它的一些常用用法。

- 选择器
    - Page 对象内置了一些用于选取节点的选择器方法，如 J 方法传入一个选择器 Selector，
    - 则能返回对应匹配的第一个节点，等价于 querySelector。
    - 如 JJ 方法则是返回符合 Selector 的列表，类似于 querySelectorAll。
    - 查看案例006
    - 如果要使用pyquery解析数据，参考001案例，先要通过返回pyquery对象：doc = pq(await page.content())
    - 使用css选择器选择节点：Firefox开发者工具找到页面元素，右键复制 CSS选择器即可
    
- 页面操作
    - 浏览器页面切换
    - 查看案例007
    - 浏览器页面操作控制，如加载、前进、后退、关闭、保存等
    - 查看案例008
    
- 点击
    - Pyppeteer 同样可以模拟点击，调用其 click 方法即可
    - click 方法第一个参数就是选择器,选择操作的节点位置，即在页面的哪个位置操作。
    - 第二个参数options是几项配置：
        - button：鼠标按钮，分为 left、middle、right。
        - clickCount：点击次数，如双击、单击等。
        - delay：延迟点击。
        - 输入文本。
    - 查看案例009
        
- 文本输入
    - 对于文本的输入，Pyppeteer 也不在话下，使用 type 方法即可
    - 查看案例010

- 获取信息
    - Page 获取源代码用 content 方法即可，
    - Cookies 则可以用 cookies 方法获取
    - page = await browser.newPage()
    - print('HTML:', await page.content())
    - print('Cookies:', await page.cookies())

- 延时等待
    - waitForSelector 方法，它可以让页面等待某些符合条件的节点加载出来再返回。
    - 在这里 waitForSelector 就是传入一个 CSS 选择器，如果找到了，立马返回结果，否则等待直到超时。
    - 查看001案例

# 4 Pyppeteer 爬虫实例
- 还是爬取 # 2 Pyppeteer 入门使用中开头分析的网址
- 网站的每个详情页的 URL 都是带有加密参数的，同时 Ajax 接口也都有加密参数和时效性，不易找出真实url接口的规律
- 针对这类动态渲染加载，加密带参数的网址推荐使用Selenium或者Pyppeteer，爬取动态渲染后的结果

- 爬取目标：
    - 遍历每一页列表页，然后获取每部电影详情页的 URL。
    - 爬取每部电影的详情页，然后提取其名称、评分、类别、封面、简介等信息。
    - 爬取到的数据存为 JSON 文件。
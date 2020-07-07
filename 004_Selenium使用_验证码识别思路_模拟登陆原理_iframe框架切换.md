#### 000_Selenium使用_参考Spider_development_study_note爬虫开发项目003文件夹和ch09文件夹的文档及案例
#### 003中的77. 动态HTML_selenium使用.md

# 1 源码中有iframe框架
- 切换 Frame
- 网页中有一种节点叫作 iframe，也就是子 Frame，相当于页面的子页面，
- 它的结构和外部网页的结构完全一致。Selenium 打开页面后，默认是在父级 Frame 里面操作，
- 而此时如果页面中还有子 Frame，Selenium 是不能获取到子 Frame 里面的节点的。
- 这时就需要使用 switch_to.frame 方法来切换 Frame

- iframe 里面的标签是无法直接选定的，必须先切换进去框架
    - 使用框架的name切换，比如QQ邮箱的登陆模块框架
    driver.switch_to.frame("login_frame")
    - 使用框架标签位置切换，比如豆瓣登陆模块框架
    driver.switch_to.frame(driver.find_elements_by_tag_name("iframe")[0])
- 切出框架，切换到外层默认框架
    driver.switch_to.default_content()   
    driver.switch_to.parent_frame() 
- 参考004豆瓣登陆案例
- 豆瓣登陆如果需要验证码，可以加入睡眠时间，然后手动填写


# 2 验证码的识别
- url不变，验证码不变
  - 请求验证码的地址，获得相应，识别

- url不变，验证码会变
  - 思路：对方服务器返回验证码的时候，会和每个用户的信息和验证码进行一个对应，之后，在用户发送post请求的时候，会对比post请求中法的验证码和当前用户真正的存储在服务器端的验证码是否相同

  - 1.实例化session
  - 2.使用session请求登录页面，获取验证码的地址
  - 3.使用session请求验证码，识别
  - 4.使用session发送post请求

- 使用selenium登录，遇到验证码
  - url不变，验证码会变，同上
  - url不变，验证码不变
    - 1.selenium请求登录页面，同时拿到验证码的地址
    - 2.获取登录页面中driver中的cookie，交给requests模块发送验证码的请求，识别
    - 3.输入验证码，点击登录
- 验证码识别详细查看：Python_prevent_spider项目04_验证码

# 3 selenium使用的注意点
- 获取文本(text)和获取属性(get_attribute)
  - 先定位到元素，然后调用`.text`或者`get_attribute`方法来取属性的值
  - 获取文本值: 每个 WebElement 节点都有 text 属性，直接调用这个属性就可以得到节点内部的文本信息
```python
from selenium import webdriver
browser=webdriver.Chrome()
url='https://dynamic2.scrape.cuiqingcai.com/'
browser.get(url)
logo=browser.find_element_by_class_name('logo-image')
print(logo)
print(logo.get_attribute('src'))
```
- 运行之后，程序便会驱动浏览器打开该页面，
- 然后获取 class 为 logo-image 的节点，最后打印出它的 src 属性
  
  
- selenium获取的页面数据是浏览器中检查可以看到的所有elements的内容，里面包含了js返回的元素，但是网页源码是没有网页内容
- 网页源码中只有一些css和js文件的引用
- find_element和find_elements的区别
    - find_element返回一个element，如果没有会报错
    - find_elements返回一个列表，没有就是空列表
    - 在判断是否有下一页的时候，使用find_elements来根据结果的列表长度来判断
- 如果页面中含有iframe、frame，需要先调用driver.switch_to.frame的方法切换到frame中才能定位元素

- selenium请求第一页的时候回等待页面加载完了之后在获取数据，但是在点击翻页之后，
    hi直接获取数据，此时可能会报错，因为数据还没有加载出来，需要time.sleep(3)
- selenium中find_element_by_class_name智能接收一个class对应的一个值，不能传入多个
    class_name传入的值有空格不能找到，被认为是符合元素了
- 建议元素定位时候使用driver.find_element_by_xpath



```
db.stu.aggregate({$group:{_id:"$name",counter:{$sum:2}}})

db.stu.aggregate({$group:{_id:null,counter:{$sum:1}}})
db.stu.aggregate({$group:{_id:"$gender",name:{$push:"$name"}}})
db.stu.aggregate({$group:{_id:"$gender",name:{$push:"$$ROOT"}}})
db.tv3.aggregate(
  {$group:{_id:{"country":"$country",province:"$province",userid:"$userid"}}},
  {$group:{_id:{country:"$_id.country",province:"$_id.province"},count:{$sum:1}}},
  {$project:{country:"$_id.country",province:"$_id.province",count:"$count",_id:0}}
  )
db.stu.aggregate(

  {$match:{age:{$gt:20}}},
  {$group:{_id:"$gender",count:{$sum:1}}}
  )
db.t2.aggregate(
  {$unwind:"$size"}
  )
db.t3.aggregate(
  {$unwind:"$tags"},
  {$group:{_id:null,count:{$sum:1}}}
  )
db.t3.aggregate(
  {$unwind:{path:"$size",preserveNullAndEmptyArrays:true}}
  )
```

# 4 Selenium 执行 JavaScript
- Selenium API 并没有提供实现某些操作的方法，
- 比如，下拉进度条。但它可以直接模拟运行 JavaScript，此时使用 execute_script 方法即可实现，代码如下：
```python
from selenium import webdriver
browser = webdriver.Chrome()
browser.get('https://www.zhihu.com/explore')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
browser.execute_script('alert("To Bottom")')
```
- 这里利用 execute_script 方法将进度条下拉到最底部，然后弹出 alert 提示框。
- 有了这个方法，基本上 API 没有提供的所有功能都可以用执行 JavaScript 的方式来实现了。


# 5 Selenium 获取 ID、位置、标签名、大小
- WebElement 节点还有一些其他属性，比如 id 属性可以获取节点 id，
- location 属性可以获取该节点在页面中的相对位置，
- tag_name 属性可以获取标签名称，
- size 属性可以获取节点的大小，也就是宽高，这些属性有时候还是很有用的。
```python
from selenium import webdriver
browser = webdriver.Chrome()
url = 'https://dynamic2.scrape.cuiqingcai.com/'
browser.get(url)
input = browser.find_element_by_class_name('logo-title')
print(input.id)
print(input.location)
print(input.tag_name)
print(input.size)
```

# 6 延时等待
- 在 Selenium 中，get 方法会在网页框架加载结束后结束执行，此时如果获取 page_source，
- 可能并不是浏览器完全加载完成的页面，如果某些页面有额外的 Ajax 请求，
- 我们在网页源代码中也不一定能成功获取到。所以，这里需要延时等待一定时间，确保节点已经加载出来。
- 这里等待的方式有两种：一种是隐式等待，一种是显式等待。

- 隐式等待
    - 当使用隐式等待执行测试的时候，如果 Selenium 没有在 DOM 中找到节点，
    - 将继续等待，超出设定时间后，则抛出找不到节点的异常。
    - 换句话说，隐式等待可以在我们查找节点而节点并没有立即出现的时候，等待一段时间再查找 DOM，默认的时间是 0。
    - implicitly_wait 方法实现了隐式等待。参考下面代码：
```python
from selenium import webdriver 
browser = webdriver.Chrome() 
browser.implicitly_wait(10) 
browser.get('https://dynamic2. scrape.cuiqingcai.com/') 
input = browser.find_element_by_class_name('logo-image') 
print(input)
```

- 显式等待
    - 隐式等待的效果其实并没有那么好，因为我们只规定了一个固定时间，而页面的加载时间会受到网络条件的影响。
    - 这里还有一种更合适的显式等待方法，它指定要查找的节点，然后指定一个最长等待时间。
    - 如果在规定时间内加载出来了这个节点，就返回查找的节点；
    - 如果到了规定时间依然没有加载出该节点，则抛出超时异常。
    - 使用案例，Python_prevent_spider的04文件夹打码平台使用
    - 示例如下：
    
```python
from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
browser = webdriver.Chrome() 
browser.get('https://www.taobao.com/') 
# 显示等待，传入浏览器，超时时间，单位秒
wait = WebDriverWait(browser, 10) 
# until等待验证，EC模块进行检测，presence_of_element_located元素是否加载处理，使用元素ID或者CSS选择器
input = wait.until(EC.presence_of_element_located((By.ID, 'q'))) 
button =  wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.btn-search'))) 
print(input, button)
```
- 首先引入 WebDriverWait 这个对象，指定最长等待时间，然后调用它的 until() 方法，传入要等待条件 expected_conditions。
- 比如，这里传入了 presence_of_element_located 这个条件，代表节点出现，其参数是节点的定位元组，也就是 ID 为 q 的节点搜索框。
- 这样做的效果就是，在 10 秒内如果 ID 为 q 的节点（即搜索框）成功加载出来，就返回该节点；如果超过 10 秒还没有加载出来，就抛出异常。
- 对于按钮，我们可以更改一下等待条件，比如改为 element_to_be_clickable，也就是可点击，
- 所以查找按钮时先查找 CSS 选择器为.btn-search 的按钮，如果 10 秒内它是可点击的，也就代表它成功加载出来了，就会返回这个按钮节点；
- 如果超过 10 秒还不可点击，也就是没有加载出来，就抛出异常。

- 等待条件，其实还有很多，比如判断标题内容，判断某个节点内是否出现了某文字等。
- 下表我列出了所有的等待条件。
- ![WebDriverWait延时等待条件](004_Selenium_模拟浏览器登陆豆瓣/007_WebDriverWait延时等待条件.png)
- [更多详细的等待条件的参数及用法介绍可以参考官方文档](http://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.support.expected_conditions)


# 7 Selenium 操作 Cookies
- 使用 Selenium，还可以方便地对 Cookies 进行操作，
- 例如获取、添加、删除 Cookies 等。示例如下：
```python
from selenium import webdriver 
browser = webdriver.Chrome() 
browser.get('https://www.zhihu.com/explore') 
print(browser.get_cookies()) 
browser.add_cookie({'name': 'name', 'domain': 'www.zhihu.com', 'value': 'germey'}) 
print(browser.get_cookies()) 
browser.delete_all_cookies() 
print(browser.get_cookies())
```
- 加载完成后，浏览器实际上已经生成 Cookies 了。
- 接着，调用 get_cookies 方法获取所有的 Cookies。然后，我们再添加一个 Cookie，这里传入一个字典，有 name、domain 和 value 等内容。
- 接下来，再次获取所有的 Cookies，可以发现，结果会多出这一项新加的 Cookie。
- 最后，调用 delete_all_cookies 方法删除所有的 Cookies。

# 8 Selenium 反屏蔽
- 很多网站都加上了对 Selenium 的检测，来防止一些爬虫的恶意爬取。
- 即如果检测到有人在使用 Selenium 打开浏览器，那就直接屏蔽。
- 其大多数情况下，检测基本原理是检测当前浏览器窗口下的 window.navigator 对象是否包含 webdriver 这个属性。
- 因为在正常使用浏览器的情况下，这个属性是 undefined，然而一旦我们使用了 Selenium，Selenium 会给 window.navigator 设置 webdriver 属性。
- 很多网站就通过 JavaScript 判断如果 webdriver 属性存在，那就直接屏蔽。

- Selenium 中，我们可以使用 CDP（即 Chrome Devtools-Protocol，Chrome 开发工具协议）来解决这个问题，
- 通过 CDP 我们可以实现在每个页面刚加载的时候执行 JavaScript 代码，执行的 CDP 方法叫作 Page.addScriptToEvaluateOnNew
- 在每次页面加载之前将 webdriver 属性置空了。
- 另外我们还可以加入几个选项来隐藏 WebDriver 提示条和自动化扩展信息，代码实现如下：
```python
from selenium import webdriver
from selenium.webdriver import ChromeOptions

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=option)
browser.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
   'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})
browser.get('https://antispider1.scrape.cuiqingcai.com/')
```
- 大多数的情况，以上的方法均可以实现 Selenium 反屏蔽。
- 但对于一些特殊的网站，如果其有更多的 WebDriver 特征检测，可能需要具体排查。

# 9 Selenium 截图
- 注意，chrome浏览器必须先截屏浏览器窗口，然后再定位截取元素，火狐浏览器定位元素后可以直接截取元素
- 火狐可以直接使用element.save_screenshot('xxx.png')

- 谷歌浏览器：
    - 1. chrome save_screenshot() 截图，可以截取整个网页。
    - 2. 利用element的size和location属性，获取element在网页(浏览器窗口)中的位置。
    - 3. 这之后用PIL下Image中的crop方法截取元素。
    - 使用案例，Python_prevent_spider的04文件夹打码平台使用,里面截取保存验证码部分
    
# 10 模拟登陆
## 10.1 登陆验证方式
- 登陆验证方式一：
    - Session + Cookies 的验证
    - Session 就是存在服务端的，里面保存了用户此次访问的会话信息，Cookies 则是保存在用户本地浏览器的，
    - 它会在每次用户访问网站的时候发送给服务器，Cookies 会作为 Request Headers 的一部分发送给服务器，
    - 服务器根据 Cookies 里面包含的信息判断找出其 Session 对象，不同的 Session 对象里面维持了不同访问用户的状态，
    - 服务器可以根据这些信息决定返回 Response 的内容。

- SSession + Cookies 的验证的两种状态
    - Cookies 里面可能只存了 Session ID 相关信息，
        - 服务器能根据 Cookies 找到对应的 Session，用户登录之后，
        - 服务器会在对应的 Session 里面标记一个字段，代表已登录状态或者其他信息（如角色、登录时间）等等，
        - 这样用户每次访问网站的时候都带着 Cookies 来访问，
        - 服务器就能找到对应的 Session，然后看一下 Session 里面的状态是登录状态，
        - 就可以返回对应的结果或执行某些操作。
    - 当然 Cookies 里面也可能直接存了某些凭证信息。
        - 比如说用户在发起登录请求之后，服务器校验通过，
        - 返回给客户端的 Response Headers 里面可能带有 Set-Cookie 字段，
        - 里面可能就包含了类似凭证的信息，这样客户端会执行 Set Cookie 的操作，
        - 将这些信息保存到 Cookies 里面，以后再访问网页时携带这些 Cookies 信息，
        - 服务器拿着这里面的信息校验，自然也能实现登录状态检测了。


- 登陆验证方式二：
    - JWT（JSON Web Token）的验证
    - 传统的基于 Session 和 Cookies 的校验也存在一定问题，
    - 比如服务器需要维护登录用户的 Session 信息，
    - 而且不太方便分布式部署，也不太适合前后端分离的项目。

- JWT 技术   
    - JWT，英文全称叫作 JSON Web Token，是为了在网络应用环境间传递声明而执行的一种基于 JSON 的开放标准。
    - 实际上就是每次登录的时候通过一个 Token 字符串来校验登录状态。
    
    - JWT 的声明一般被用来在身份提供者和服务提供者间传递被认证的用户身份信息，
    - 以便于从资源服务器获取资源，也可以增加一些额外的其他业务逻辑所必须的声明信息，
    - 所以这个 Token 也可直接被用于认证，也可传递一些额外信息。
    
    - JWT，一些认证就不需要借助于 Session 和 Cookies 了，服务器也无需维护 Session 信息，减少了服务器的开销。
    - 服务器只需要有一个校验 JWT 的功能就好了，同时也可以做到分布式部署和跨语言的支持。

- JWT 字符串说明   
    - JWT 通常就是一个加密的字符串，它也有自己的标准，类似下面的这种格式：
    - eyJ0eXAxIjoiMTIzNCIsImFsZzIiOiJhZG1pbiIsInR5cCI6IkpXVCIsImFsZyI6IkhTMjU2In0.eyJVc2VySWQiOjEyMywiVXNlck5hbWUiOiJhZG1pbiIsImV4cCI6MTU1MjI4Njc0Ni44Nzc0MDE4fQ.pEgdmFAy73walFonEm2zbxg46Oth3dlT02HR9iVzXa8
    - 字符串中间有两个“.”来分割开，可以把它看成是一个三段式的加密字符串。
    - 它由三部分构成，分别是 Header、Payload、Signature：
        - Header，声明了 JWT 的签名算法，如 RSA、SHA256 等等，也可能包含 JWT 编号或类型等数据，然后整个信息 Base64 编码即可。
        - Payload，通常用来存放一些业务需要但不敏感的信息，如 UserID 等，另外它也有很多默认的字段，如 JWT 签发者、JWT 接受者、JWT 过期时间等等，Base64 编码即可。
        - Signature，这个就是一个签名，是把 Header、Payload 的信息用秘钥 secret 加密后形成的，这个 secret 是保存在服务器端的，不能被轻易泄露。这样的话，即使一些 Payload 的信息被篡改，服务器也能通过 Signature 判断出来是非法请求，拒绝服务。

- JWT 验证流程
    - 登录认证流程也很简单了，用户拿着用户名密码登录，然后服务器生成 JWT 字符串返回给客户端，
    - 客户端每次请求都带着这个 JWT 就行了，服务器会自动判断其有效情况，如果有效，那自然就返回对应的数据。
    - 但 JWT 的传输就多种多样了，可以放在 Request Headers，也可以放在 URL 里，
    - 甚至有的网站也放在 Cookies 里，但总而言之，能传给服务器校验就好了。
    
## 10.2 Session + Cookies 模拟登陆
- 基于 Session 和 Cookies 的模拟登录，如果我们要用爬虫实现的话，
- 其实最主要的就是把 Cookies 的信息维护好，因为爬虫就相当于客户端浏览器，我们模拟好浏览器做的事情就好了

- 模拟登陆的三种方式：
    - 方式1：已经手动登录过账号
        - 如果我们已经在浏览器里面登录了自己的账号，我们要想用爬虫模拟的话，
        - 可以直接把 Cookies 复制过来交给爬虫就行了，这也是最省事省力的方式。
        - 这就相当于，我们用浏览器手动操作登录了，然后把 Cookies 拿过来放到代码里面，
        - 爬虫每次请求的时候把 Cookies 放到 Request Headers 里面，
        - 就相当于完全模拟了浏览器的操作，服务器会通过 Cookies 校验登录状态，
        - 如果没问题，自然可以执行某些操作或返回某些内容了。
    - 方式2：爬虫模拟登陆过程
        - 如果我们不想有任何手工操作，可以直接使用爬虫来模拟登录过程。
        - 需要分析真实的请求地址，一些地址存在加密和各种参数，分析较难
        - 登录的过程其实多数也是一个 POST 请求，我们用爬虫提交用户名密码等信息给服务器，
        - 服务器返回的 Response Headers 里面可能带了 Set-Cookie 的字段，我们只需要把这些 Cookies 保存下来就行了。
        - 所以，最主要的就是把这个过程中的 Cookies 维护好就行了。
        - 当然这里可能会遇到一些困难，比如登录过程还伴随着各种校验参数，不好直接模拟请求，
        - 也可能网站设置 Cookies 的过程是通过 JavaScript 实现的，
        - 所以可能还得仔细分析下其中的一些逻辑，尤其是我们用 requests 这样的请求库进行模拟登录的时候，遇到的问题可能比较多。
    - 方式3：自动化测试工具模拟登陆
        - (上面爬虫无法模拟的登陆一般使用 Selenium 或 Pyppeteer 可以实现模拟登陆，只是效率低一些而已)
        - 我们也可以用一些简单的方式来实现模拟登录，即把人在浏览器中手工登录的过程自动化实现，
        - 比如我们用 Selenium 或 Pyppeteer 来驱动浏览器模拟执行一些操作，
        - 如填写用户名、密码和表单提交等操作，等待登录成功之后，
        - 通过 Selenium 或 Pyppeteer 获取当前浏览器的 Cookies 保存起来即可。
        - 然后后续的请求可以携带 Cookies 的内容请求，同样也能实现模拟登录。
    - 上面3种方式的目的就是维护好客户端的 Cookies 信息，然后每次请求都携带好 Cookies 信息就能实现模拟登录了
    
## 10.3 JWT 模拟登陆
- 基于 JWT 的真实情况也比较清晰了，由于 JWT 的这个字符串就是用户访问的凭证，那么模拟登录只需要做到下面几步即可：
    - 第一，模拟网站登录操作的请求，比如携带用户名和密码信息请求登录接口，获取服务器返回结果，这个结果中通常包含 JWT 字符串的信息，保存下来即可。
    - 第二，后续的请求携带 JWT 访问即可，一般情况在 JWT 不过期的情况下都能正常访问和执行对应的操作。携带方式多种多样，因网站而异。
    - 第三，如果 JWT 过期了，可能需要重复步骤一，重新获取 JWT。
    - 关键还是需要先用户登录一次，获取 JWT ，和上面的获取 Cookies 一样。
    - 当然这个模拟登录的过程也肯定带有其他的一些加密参数，需要根据实际情况具体分析。
    
## 10.4 模拟登录优化方案 （账号防封）
- 问题：
    - 如果爬虫要求爬取的数据量比较大或爬取速度比较快，
    - 而网站又有单账号并发限制或者访问状态检测并反爬的话，
    - 可能我们的账号就会无法访问或者面临封号的风险了。这时候一般怎么办呢？
- 解决方法：
    - 我们可以使用分流的方案来解决，比如某个网站一分钟之内检测一个账号只能访问三次或者超过三次就封号的话，
    - 我们可以建立一个账号池，用多个账号来随机访问或爬取，这样就能数倍提高爬虫的并发量或者降低被封的风险了。
    - 比如在访问某个网站的时候，我们可以准备 100 个账号，然后 100 个账号都模拟登录，
    - 把对应的 Cookies 或 JWT 存下来，每次访问的时候随机取一个来访问，
    - 由于账号多，所以每个账号被取用的概率也就降下来了，
    - 这样就能避免单账号并发过大的问题，也降低封号风险。

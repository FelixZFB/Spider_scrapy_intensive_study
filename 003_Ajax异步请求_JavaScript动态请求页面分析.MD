# 动态页面解析重点难点汇总

# 1. 静态页面解析
- 互联网一部分网页都是静态页面,比如常见的论坛，51job，sht论坛等
- 具体静态页面请求解析参考爬虫开发项目和TZKT里面的项目
- 静态请求页面特征：
    - 查看网页源码，网页中显示的内容直接在源码中都可以找到
    - 检查里面的elements里面有所有内容（此处动态页面的elements也是有完整的内容）
    - 使用Chrome的network查看，请求列表中的第一个网址，就是请求的网址
    - 查看response里面也有所有的静态页面内容 
    - 静态页面解析直接通过Chrome或者Firefox的查看elements和选择页面的元素
    - 进行定位解析
    - 网址和页面内容都有一定的规律

# 2. JavaScript 动态页面解析
- 动态页面，请求一个网址，返回的页面内容是通过另外一个js请求渲染生成的
- 无法直接找到请求的真实地址和源码内容，需要进行分析才能找出真实地址和响应内容

- 参考图片放在003哔哩哔哩文件夹中
- 动态请求页面特征：
    - 源码中并没有页面中的内容，network的第一个网址也不是返回页面内容的真实网址  
    - 以哔哩-鬼畜-鬼畜调教为例：[https://www.bilibili.com/v/kichiku/guide/?spm_id_from=333.5.b_7375626e6176.2#/all/default/0/1/]
    - 查看网页源码,里面并没有我们看见浏览器页面中的内容，比如源码搜索页面中的8848没有结果，参考图片004
    - network查看，第一个网址并不是返回页面的真实地址，第一个网址的response里面搜索8848也没有结果，参考图片005
    - 页面和Elements中都可以查看找8848，参考图片006
    
- 如何寻找页面响应的真实地址和响应内容：
    # 1. 查找响应真实地址
    - 方法1：Chrome的search工具
    - 使用开发工具栏右上角里面的search,相当与全局搜索(搜索有代表性的英文或者数字，不要搜汉字，汉字有些会是其它编码)
    - 比如搜索8848，哔哩网页内容更新很快，就在我写这个时候，8848已经被刷新到第2页中了，参考图片007
    - 此时有3个结果，我们在name网址列表中ctrl+f搜索首单词region和newlist
    - 左边结果中选择region结果下面的第二行可以选中网址列表中的网址，然后查看response，
    - 点击response左下角的{}格式化json内容，我们可以先拉动一下可以发现内容很少，可能不是响应内容
    - 搜索8848,只有一个结果，并且不是页面中的8848，参考图片008
    - 同样，搜索newlist，只有一个网址对应，查看响应内容，8848里面正好3个结果，和页面内容相同参考图片009
    - newlist就是js渲染返回响应内容的真实地址
    
    - 方法2：
    - Chrome不断请求的新页面地址是放在url列表最下面的
    - 可以多请求几页，打开过滤器filter,Preserve log勾选上代表发送新的请求时候不清楚前面请求的记录
    - 上面filter过滤选择JS(请求的是一个JavaScript文件)即可，观察下面网址变化，也可以找出规律，每切换一个页面会多一个newlist请求
    - 并且可以发现里面的网址参数都是有规律变化，只有一个pn=x在变化，即页面，查看图片010
    - 通过查看请求的url列表也可以找到真实的页面响应地址
    
    # 2. 查看响应内容
    - 查看响应内容：
        - newlist中的就是json格式的响应内容
        - 查看newlist的headers:
        - requests headers里面的：https://www.bilibili.com/v/kichiku/guide/?spm_id_from=333.6.b_7375626e6176.2
        - url是最原始的地址，但是和浏览器url栏中还是不同，复制进去打开就还是该页面
        - response headers里面可以看到响应内容是json格式：Content-Type: application/json; charset=utf-8
        - General中可以看到接近真实的地址：Request URL: https://api.bilibili.com/x/web-interface/newlist?callback=jqueryCallback_bili_4722156102796&rid=22&type=0&pn=2&ps=20&jsonp=jsonp&_=1568290229435
        - 上面url地址直接打开是错误的,里面有callback参数后面还有json参数，删除的时候前后的的&符号要删掉
        - 删掉callback回调方法才是真实网址，保留后面的参数，最后的json部分可以不删，为了简洁都删了
        - 真正的JS渲染得到页面的网址：
            https://api.bilibili.com/x/web-interface/newlist?&rid=22&type=0&pn=2&ps=20
            - 打开该网址，响应页面的json字符串就显示出来了，查看图片011
            - 先安装Chrome的格式化json字符串插件，参考网址：https://blog.csdn.net/wust_lh/article/details/87189044
            - 安装软件和说明放在hello world 的software中，安装插件后打开json直接就格式化了，查看012
    
    - 我们可以观察网址，pn=2就是第二页，可以修改这个数字，就可以得到不同页面的响应内容json数据
    - 我们可以换几个栏目，查看newlist地址的规律
        - 先看鬼畜各个栏目：
        - 鬼畜下的鬼畜调教： https://api.bilibili.com/x/web-interface/newlist?&rid=22&type=0&pn=1&ps=20
        - 鬼畜下的音MAD:    https://api.bilibili.com/x/web-interface/newlist?rid=26&type=0&pn=1&ps=20
        - 鬼畜下的人力:：   https://api.bilibili.com/x/web-interface/newlist?rid=126&type=0&pn=1&ps=20
        - 只有rid不同，rid当前鬼畜下的各个分类
        
        - 再看手机栏目：
        - 手机平板：https://api.bilibili.com/x/web-interface/newlist?rid=95&type=0&pn=1&ps=20
        - 电脑装机：https://api.bilibili.com/x/web-interface/newlist?rid=189&type=0&pn=1&ps=20
        
        - 通过以上规律发现所有栏目，就是rid的数字不同而已，其它都相同，ps type可能是一些请求服务器使用的参数不用管
        
    # 3. 分析响应内容
    - 分析json内容 
    - archives里面有20个，正是1个页面的20个视频，下面也有size为20，参考图片013
    - 展开一个archives就是一个视频的详细信息，标题，作者，图片链接
    - 视频的地址，我们先查看页面内容elements里面有视频连接，或者直接打开视频链接，发现每个视频链接就是里面的数字不同
        https://www.bilibili.com/video/av67403285/
        https://www.bilibili.com/video/av67408718/
    - 在json里面查找数字，发现就是json的aid对应的数字，提取出aid的值就也可以拼接得到原始网址了
    - 参考图片014和015
    
    # 4. 提取响应内容
    - 请求该真实地址
    - 下载响应的loads的json内容为python的字典格式
    - 然后使用正则re查找需要的内容，标题，作者，视频编号
   
    - 参考：016_哔哩哔哩视频爬取_请求js内容_查找视频标题编号作者等信息
    - url的rid即视频栏目，pn即栏目下的视频页码，通过修改这两个参数就可以爬取所有的视频信息

# 3. Ajax 异步请求   
- 发送 Ajax 请求到网页更新的过程可以简单分为以下 3 步：
    - 发送请求
    - 解析内容
    - 渲染网页

## 3.1 Ajax 异步请求原理
- 发送请求
    - 我们知道 JavaScript 可以实现页面的各种交互功能，Ajax 也不例外，
    - 它是由 JavaScript 实现的，实际上执行了如下代码：
```javascript
    var xmlhttp;
    if (window.XMLHttpRequest) {
        //code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();} 
    else {//code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xmlhttp.onreadystatechange=function() {if (xmlhttp.readyState==4 && xmlhttp.status==200) {document.getElementById("myDiv").innerHTML=xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST","/ajax/",true);
    xmlhttp.send();
```
- 请求执行过程：
    - JavaScript 对 Ajax 最底层的实现，这个过程实际上是新建了 XMLHttpRequest 对象，
    - 然后调用 onreadystatechange 属性设置监听，最后调用 open() 和 send() 方法向某个链接（也就是服务器）发送请求。
    - 前面我们用 Python 实现请求发送之后，可以得到响应结果，但这里请求的发送由 JavaScript 来完成。
    - 由于设置了监听，所以当服务器返回响应时，onreadystatechange 对应的方法便会被触发，
    - 我们在这个方法里面解析响应内容即可。
    
- 解析内容
    - 得到响应之后，onreadystatechange 属性对应的方法会被触发，
    - 此时利用 xmlhttp 的 responseText 属性便可取到响应内容。
    - 这类似于 Python 中利用 requests 向服务器发起请求，然后得到响应的过程。
    - 返回的内容可能是 HTML，也可能是 JSON，接下来我们只需要在方法中用 JavaScript 进一步处理即可。
    - 比如，如果返回的内容是 JSON 的话，我们便可以对它进行解析和转化。

- 渲染网页
    - JavaScript 有改变网页内容的能力，解析完响应内容之后，就可以调用 JavaScript 针对解析完的内容对网页进行下一步处理。
    - 比如，通过 document.getElementById().innerHTML 这样的操作，对某个元素内的源代码进行更改，这样网页显示的内容就改变了，
    - 这种对 Document 网页文档进行如更改、删除等操作也被称作 DOM 操作。
    - 上例中，document.getElementById("myDiv").innerHTML=xmlhttp.responseText这个操作便将 ID 为 myDiv 的节点内部的 HTML 代码更改为服务器返回的内容，
    - 这样 myDiv 元素内部便会呈现出服务器返回的新数据，网页的部分内容看上去就更新了。
    - 可以看到，发送请求、解析内容和渲染网页这 3 个步骤其实都是由 JavaScript 完成的。
    - 我们再回想微博的下拉刷新，这其实是 JavaScript 向服务器发送了一个 Ajax 请求，然后获取新的微博数据，将其解析，并将其渲染在网页中的过程。
    - 因此，真实的数据其实都是通过一次次 Ajax 请求得到的，如果想要抓取这些数据，我们需要知道这些请求到底是怎么发送的，发往哪里，发了哪些参数。
    
## 3.2 Ajax 异步请求分析
- 微博网址为例：https://m.weibo.cn/u/2830678474
    - 拖动刷新的内容由 Ajax 加载，而且页面的 URL 没有变化，这时我们应该到哪里去查看这些 Ajax 请求呢？
    - Chrome或者Firefox 浏览器打开微博链接，随后在页面中点击鼠标右键，从弹出的快捷菜单中选择“检查” 选项，此时便会弹出开发者工具
    - 选择network，勾选上 Preserve Log 持续记录已经访问过的请求，filter过滤器勾选XHR，Ajax 有其特殊的请求类型，它叫作 xhr。
    - 在图中我们可以发现一个以 getIndex 开头的请求，其 Type 为 xhr，这就是一个 Ajax 请求。用鼠标点击这个请求，可以查看这个请求的详细信息。
    - 在详情中可以观察到 Request Headers、URL 和 Response Headers 等信息。Request Headers 中有一个信息为 X-Requested-With:XMLHttpRequest，这就标记了此请求是 Ajax 请求
    - 查看003文件夹中017/018图片，不停向下滚动，每次动态加载页面，就会出现一个xhr类型的请求

- Ajax 请求理解：
    - 没有Ajax时，发送请求获取响应，就需要将所有html内容一次返回，所以可以用requests进行请求，
    - 有了Ajax就是第一次请求只返回了一部分信息，如页面框架内容，而没有数据，
    - 触发了Ajax请求后，又发送了一次请求，得到json格式数据进行解析后填充到页面上。
    - 后续如果滑动时又触发了Ajax请求，来刷新页面。
    - 可以把Ajax看做是满足一定条件后自动触发的请求，其实质也是一种请求，只不过是js来发起的罢了。
    - 一般来说没有 Ajax 的话，html 会是服务端直接渲染出来，结果会在 html 里面，所以 reqeusts 直接抓。
    - 有 Ajax 一般都是后期渲染，所以最开始的 html 里面没东西，所以要分析 Ajax。
    
## 3.3 Ajax 动态请求实例
- 演示网址：https://dynamic1.scrape.cuiqingcai.com/

- 页面分析：
    - 查看网页源码，里面并没有网页数据，只有一些js引用代码
    - 不断切换页面，network中选择查看xhr类型的请求，发现没选择一页，就会有一个xhr请求，进入请求地址里面
    - 发现就是页面的的数据，数据格式是json格式，一般ajax请求的数据格式都是json格式
    - 并且网址具有规律，只有offset的值不同，0显示第1-10条数据，10显示第11-20条数据，依次类推
    - 查看003文件夹中019图片
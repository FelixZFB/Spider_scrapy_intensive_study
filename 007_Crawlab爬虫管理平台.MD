## Crawlab爬虫管理平台安装及使用教程

# 1 爬虫管理平台的定义
## 1.1 狭义的爬虫管理平台
- 爬虫管理平台是一个一站式管理系统，集爬虫部署、任务调度、任务监控、结果展示等模块于一体，
- 通常配有可视化 UI 界面，可以在 Web 端通过与 UI 界面交互来有效管理爬虫。
- 爬虫管理平台一般来说是支持分布式的，可以在多台机器上协作运行。

## 1.2 广义的爬虫管理平台
- 后羿采集器、八爪鱼、聚合数据

# 2 为什么需要爬虫管理平台？
- 有了爬虫管理平台，开发者特别是爬虫工程师就能够方便的添加爬虫、执行任务、查看结果，
- 而不用在命令行之间来回切换，非常容易出错。
- 一个常见的场景就是爬虫工程师最初技术选型用了 scrapy 和 crontab 来管理爬虫任务，
- 他不得不小心翼翼的选择定时任务的时间区间，以至于不会将服务器 CPU 或内存占满；
- 更棘手的问题是，他还需要将 scrapy 产生的日志存到文件里，
- 一旦爬虫出错了，他不得不用 shell 命令一个一个来查看日志来定位错误原因，严重时会花上一个整天；
- 还有个严重的问题，爬虫工程师可能发现公司业务量在增加，他需要写上百个爬虫来满足公司的业务需求，
- 而用 scrapy 和 crontab 来管理完全就是个噩梦。

# 2 爬虫管理平台的模块
[爬虫管理平台模块](099_爬虫相关图片解释/034_爬虫管理平台模块.png)
- 爬虫管理平台的模块主要包含以下内容：
    - 任务管理：如何执行、调度爬虫抓取任务，以及如何监控任务，包括日志监控等等；
    - 爬虫管理：包括爬虫部署，即将开发好的爬虫部署（打包或复制）到相应的节点上，以及爬虫配置和版本管理；
    - 节点管理：包括节点（服务器/机器）的注册和监控，以及节点之间的通信，如何监控节点性能状况等；
    - 前端应用：包括一个可视化 UI 界面，让用户可通过与其交互，与后台应用进行通信。
- 当然，有些爬虫管理平台可能还不止这些模块，它可能包括其他比较实用的功能，
    - 例如可配置的抓取规则、可视化配置抓取规则、代理池、Cookie 池、异常监控等等。
    
# 3 现有爬虫管理平台
[现有爬虫管理平台对比](099_爬虫相关图片解释/035_现有爬虫管理平台对比.png)
- 重度 scrapy 爬虫依赖的、又不想折腾的开发者，可以考虑 Scrapydweb；
- 而对于有各种类型的、复杂技术结构的爬虫开发者来说，应该优先考虑更灵活的 Crawlab。


# 4 Crawlab爬虫管理平台
- Crawlab 是基于 Golang 的分布式爬虫管理平台，支持 Python、NodeJS、Java、Go、PHP 等多种编程语言以及多种爬虫框架。
- Crawlab 主要解决的是大量爬虫管理困难的问题，例如需要监控上百个网站的参杂 scrapy 和 selenium 的项目不容易做到同时管理，而且命令行管理的成本非常高，还容易出错。
- Crawlab 支持任何语言和任何框架，配合任务调度、任务监控，很容易做到对成规模的爬虫项目进行有效监控管理。

- 项目GitHub地址：https://github.com/crawlab-team/crawlab
- 官方文档地址：https://docs.crawlab.cn/

## 4.1 Crawlab环境安装
- 1 安装docker
    - Ubuntu虚拟机中安装docker：docker-ce docker-ce-cli docker-compose
    - 具体安装步骤参考：[Ubuntu18.04 安装及使用Docker（安装常见报错及Docker常用命令）](https://blog.csdn.net/u011318077/article/details/104733149)
    - docker全部安装完成后，镜像源修改中国的源地址，终端执行命令创建 sudo vi /etc/docker/daemon.json 文件，在其中输入如下内容。
        
        {
          "registry-mirrors": ["https://registry.docker-cn.com"]
        }
        
        - 然后输入:符号，输入wq保存退出
    - Ubuntu安装使用Docker注意：
        - Docker安装完成后，如果不修改源，网速不好，有时候启动或者执行命令会出现失败或者超时提示
        - 安装博文中提到卸载后重新安装，后面发现是网速问题，只需要新建daemon.json文件，添加中国源即可
        - 注意，有些命令需要使用sudo docker xxx xxx ... 执行，直接docker执行会报错
        - 也可以将终端使用 su 回车 输入超级用户密码 回车 进入超级用户 显示符号位#
    
    - Docker安装注意事项:
        - Docker桌面版，WIN10系统只能专业版和企业版可以安装
        - 家庭版安装比较麻烦，需要视同toolbox工具或者修改注册表伪装为专业版骗过软件安装时候的检测
        - Docker安装在WIN10下面需要开启HyperV虚拟功能，该功能开启后会导致VMware和VirtualBox出错
        - 鉴于以上原因，不推荐在WIN10安装Docker,建议Ubuntu虚拟机服务器中安装
        - Win10安装可以具体参考我的QQ浏览器收藏夹中，python相关软件安装/docker安装，里面有家庭版和专业版安装收藏
    

- 2 下载 Crawlab 的镜像
    - 官方文档命令：sudo docker pull tikazyq/crawlab:latest  下载超时，网络有问题
    - 使用以下最新源地址：
        - sudo docker pull registry.cn-hangzhou.aliyuncs.com/crawlab-team/crawlab:latest
    - [docker下载crawlab镜像](099_爬虫相关图片解释/036_docker下载crawlab镜像.png)
    - docker images   查看已有镜像的具体信息   
    - REPOSITORY                                               TAG                 IMAGE ID            CREATED             SIZE
    - registry.cn-hangzhou.aliyuncs.com/crawlab-team/crawlab   latest              d9132fa22f35        2 weeks ago         710MB
    - hello-world                                              latest              fce289e99eb9        15 months ago       1.84kB

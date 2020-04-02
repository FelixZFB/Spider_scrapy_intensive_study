## Crawlab爬虫管理平台安装及使用教程

---

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

---

# 4 Crawlab爬虫管理平台
- Crawlab 是基于 Golang 的分布式爬虫管理平台，支持 Python、NodeJS、Java、Go、PHP 等多种编程语言以及多种爬虫框架。
- Crawlab 主要解决的是大量爬虫管理困难的问题，例如需要监控上百个网站的参杂 scrapy 和 selenium 的项目不容易做到同时管理，而且命令行管理的成本非常高，还容易出错。
- Crawlab 支持任何语言和任何框架，配合任务调度、任务监控，很容易做到对成规模的爬虫项目进行有效监控管理。

- 项目GitHub地址：https://github.com/crawlab-team/crawlab
- 官方文档地址：https://docs.crawlab.cn/

## 4.1 Crawlab 部署安装
### 4.1.1 安装docker
- Ubuntu虚拟机中安装docker：docker-ce docker-ce-cli docker-compose
    - 具体安装步骤参考：[Ubuntu18.04 安装及使用Docker（安装常见报错及Docker常用命令）](https://blog.csdn.net/u011318077/article/details/104733149)
- docker全部安装完成后，镜像源修改中国的源地址，终端执行命令创建 sudo vi /etc/docker/daemon.json 文件，在其中输入如下内容。
   
        {
          "registry-mirrors": ["https://registry.docker-cn.com"]
        }
 
    - 然后输入:符号，输入wq保存退出

- docker-compose安装注意：
- 上面直接使用 apt install  docker-compose 安装的版本不是最新的，只是1.17
    - sudo apt remove docker-compose 卸载掉 1.17 版本
    - 然后先安装 pip 工具： sudo apt install python-pip
    - pip工具有pip 和 pip3 只安装pip即可
    - 由于系统已经安装了anaconda3，上面安装 pip 默认安装在 anaconda3 python3.7 下面
    - 下面使用pip安装的包，也都会在anaconda3里面，所以下面启动需要创建软连接
    - pip安装参考[Ubuntu上安装pip及使用pip安装包](https://linux.cn/article-10110-1.html)  
    - pip install docker-compose    前提 Ubuntu 系统里面要已经安装了 python3 版本
    - 安装后的 docker-compose 是在 anaconda3 里面 ，需要建立软连接到 /usr/bin 目录下面，才能直接终端运行命令
    - sudo ln -s /home/felix/anaconda3/bin/docker-compose /usr/bin/docker-compose 
    - [](008_Docker容器/026_安装pip工具_pip安装docker-compose最新版.png)
    - 安装完成并且软连接以后，使用以下命令查看是否成功：
        - docker-compose --version  
        - docker-compose ps   查看docker-compose容器，该命令需要先在用户下面创建一个 crawlab 文件夹，然后创建 yml 文件并写入配置，才能使用该命令
    

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

### 4.1.2 下载 Crawlab 的镜像
- 官方文档命令：sudo docker pull tikazyq/crawlab:latest  下载超时，网络有问题
- 使用以下最新源地址：
    - docker pull tikazyq/crawlab:latest    dockerhub官方下载镜像
    - sudo docker pull registry.cn-hangzhou.aliyuncs.com/crawlab-team/crawlab:latest  阿里云
- [docker下载crawlab镜像](099_爬虫相关图片解释/036_docker下载crawlab镜像.png)
- docker images   查看已有镜像的具体信息   
    - REPOSITORY                                               TAG                 IMAGE ID            CREATED             SIZE
    - registry.cn-hangzhou.aliyuncs.com/crawlab-team/crawlab   latest              d9132fa22f35        2 weeks ago         710MB
    - hello-world                                              latest              fce289e99eb9        15 months ago       1.84kB
    
### 4.1.3 启动crawlab
- 先保证上面 docker docker-compose 安装成功
- crawlab镜像已下载到本地
- crawlab启动步骤：  
    - 在用户下面创建一个 crawlab 文件夹，切换到该文件夹下面
    - 该文件下创建一个 docker-compose.yml 文件，填入配置内容
    - 具体配置查看[Docker 安装部署](https://docs.crawlab.cn/Installation/Docker.html)
    - 以及[如何快速搭建实用的爬虫管理平台](https://gitbook.cn/books/5d4ea403664ff37af8176bde/index.html)
    - [yaml配置文件详细说明](https://docs.crawlab.cn/Config/)
    - 执行容器启动命令：docker-compose up 或者 docker-compose up -d (后台运行)
    - 第一次运行上述命令后，Docker Compose 会去拉取 MongoDB 和 Redis 的镜像，
    - 这可能会花几分钟时间。拉取完毕后，四个服务会依次启动，您将会在命令行中看到4个done 并且开始打印log日志信息
    - 并且浏览器中输入http://localhost:8080，就会进入 crawlab 登陆界面(用户名：admin 密码：admin)
    - [](008_Docker容器/027_docker-compose首次运行crawlab_自动下载安装依赖环境镜像.png)
    - [](008_Docker容器/028_pip安装位置_docker-compose安装位置.png)
    - [](008_Docker容器/029_docker-compose启动crawlab_启动成功.png)
    - [](008_Docker容器/031_crawlab网页登录界面.png)
    
    - 退出容器终端，使用 ctrl + z
    - 此时 docker-compose ps 查看容器都在后台运行
    - 停止并删除 crawlab 容器：docker-compose down
    - 终端命令先是 stop 然后 remove
    - 我们也可以停止容器不删除，下次直接启动,停止后再删除：
        - docker-compose stop  
        - docker-compose start
        - docker-compose rm
    - 此时 docker-compose ps 查看，没有容器相关信息
    - 更多 docker-compose 命令查看[Docker使用教程](008_Docker使用教程.MD)
    - [](008_Docker容器/032_停止并删除crawlab容器.png)
    
- 再次启动crawlab：
    - 由于docker容器很小，可以每次用完删除，下次再次直接启动一个新的
    - 先切换到用户felix下面的crawlab文件夹，执行启动命令：docker-compose up 
    - 由于首次启动，crawlab依赖的mongo和redis镜像已经拖取到本地docker了，再次启动迅速启动完成
    - [](008_Docker容器/033_再次启动crawlab容器.png)
    
- 当 Crawlab 有更新时，我们会将新的变更构建更新到新的镜像中。
    - 最新的镜像名称都是 tikazyq/crawlab:latest。
    - 而一个指定版本号的镜像名称为 tikazyq/crawlab:<version>，
    - 例如 tikazyq/crawlab:0.4.7 为 v0.4.7 版本对应的镜像。
    - 拉取最新镜像
        - docker pull tikazyq/crawlab:latest
    - 日常启动 Docker 容器，后台执行
        - docker-compose up -d
        
- crawlab 环境部署注意点：
- 注意点1：
    - docker-compose.yml 配置文件
    - 需要注意CRAWLAB_API_ADDRESS这个环境变量，很多初学使用者都是因为该变量配置不正确而导致无法登陆。
    - CRAWLAB_API_ADDRESS: "localhost:8000"  # 前端调用的 API 地址，默认为 localhost:8000
    - 避免该端口被其它进程占用，一般不用做修改
- 注意点2：
    - 本机上启动的 Docker Compose，可以在浏览器中输入http://localhost:8080，然后就能看到登陆界面了；
    - 如果您是在其他机器上启动的 Docker Compose，您需要在本机的浏览器中输入http://<your_ip>:8080来看到登陆界面，
    - <your_ip>是其他机器(启动 Docker Compose 的机器)的 IP 地址（请保证 8080 端口在该机器已对外开放）。
- 注意点3：
    - 初始登陆用户名密码是 admin/admin，您可以使用这个用户名密码来登陆。
    - 如果您的环境变量CRAWLAB_API_ADDRESS设置得不正确，
    - 您可能会看到点击登陆后登陆按钮会一直转圈而没有任何提示。
    - 这时请重新在docker-compose.yml中设置正确的CRAWLAB_API_ADDRESS（将localhost替换为<your_ip>），
    - 重新启动docker-compose up。然后在浏览器中输入http://<your_ip>:8080。
  
    
### 4.1.4 安装 CLI 命令行工具
- [CLI 命令行工具](https://docs.crawlab.cn/SDK/CLI.html)
- 安装 CLI 之前，您需要确保您用的 Python 版本是 3.6 以上，否则将可能会在使用中出现错误
- 打开一个新的终端，执行以下命令
    - pip install crawlab-sdk
    - ![](007_Crawlab爬虫管理平台/002_安装CLI命令行工具_crawlab-sdk安装.png)
    - ![](007_Crawlab爬虫管理平台/003_安装CLI命令行工具_crawlab-sdk安装完成.png)
- 安装完成后，需要登录 crawlab 后端，执行以下命令
    - 登录并输入参数
        - crawlab login -u <username> -a <api_address>
    - 例子
        - crawlab login -u admin -a http://localhost:8080/api
        - 然后会要求输入登录密码：admin
        - 注意：登录之前，不要打开 http://localhost:8080 ，并登陆进去，如果打开或者已经网页手动登陆进去此处输入密码会提示错误
        - ![](007_Crawlab爬虫管理平台/004_CLI命令上传项目的crawlab管理平台.png)   
    - 如果登录成功，CLI 会将用户名、密码、API 地址和获取到的 Token 保存在本地，供后面使用。
    - 注意：这里的 <api_address> 是后端 API 的地址。如果您是用的 Docker 镜像，只需要在 Web 界面 URL 后加一个 /api 后缀就可以了。
    - 例如，如果您访问 Web 的地址是 http://localhost:8080，您的 <api_url> 就是 http://localhost:8080/api

- CLI常用命令：

- 上传爬虫：
    - 上面登陆成功后，切换到爬虫项目文件夹下，即 scrapy.cfg 同级文件夹, 分别执行以下命令：
        - cd /home/felix/crawlab/tieba      切换文件夹
        - crawlab upload                    上传爬虫项目
    - 如果不传参数，CLI 会将当前整个目录打包成 zip 文件并上传的，不是很安全，因此并不推荐此做法。
    - 上传成功后，浏览器打开 http://localhost:8080 自动跳转到管理界面，可以看到已经成功上传的爬虫
    - 当然，如果您想进行更复杂的上传爬虫操作，可以采用下面的命令。
    - 上传指定目录并附带爬虫名称、显示名称、结果集等信息
    
    ```
    crawlab upload \
    -n <spider_name> \ # 爬虫名称, \ 表示换行 < > 不需要写
    -N <display_name> \ # 显示名称
    -m <execute_command> \ # 执行命令
    -c <result_collection> # 结果集
    ```
    - 参数说明：
        - 爬虫名称：爬虫的唯一识别名称（spiders中写的爬虫名name，唯一的用于scrapy crawl xxx），将会在爬虫根目录中创建一个该名称的文件目录，因此建议为没有空格和特殊符号的小写英文，可以带下划线；
        - 显示名称：爬虫显示在前端的名称，可以为任何字符串，爬虫管理平台展示的爬虫名称；
        - 执行命令：爬虫将在 shell 中执行的命令，最终被执行的命令将为 执行命令 和 参数 的组合；
        - 结果集：集合的名称，爬虫抓取结果储存在 MongoDB 数据库里的集合（Collection），类似于 SQL 数据库中的表（Table）。
       
    - 如果您想针对某一个爬虫 ID 上传爬虫，只需要指定 -i 这个命令，将爬虫 ID 传入就可以了，CLI 将上传爬虫并覆盖其爬虫文件。
    - 具体的爬虫上传 CLI 帮助，请查看 crawlab upload --help    
    
- 查看节点列表
    - crawlab nodes
- 查看爬虫列表
    - crawlab spiders
- 查看任务列表
    - crawlab tasks
- 查看定时任务列表
    - crawlab schedules    
    
    
## 4.2 Crawlab上传运行爬虫项目
## 4.2.1 requests 普通爬虫 (不推荐)
- 参考文档：
    - [自定义爬虫-使用CLI命令行工具上传爬虫](https://docs.crawlab.cn/Spider/CustomizedSpider.html)
    - [可配置爬虫--功能是基于scrapy的](https://docs.crawlab.cn/Spider/ConfigurableSpider.html) 
- 不推荐，不做详细介绍

## 4.2.2 scrapy 爬虫 (推荐)
- 参考文档：
    - [自定义爬虫-使用CLI命令行工具上传爬虫](https://docs.crawlab.cn/Spider/CustomizedSpider.html)
    - [Scrapy 爬虫详细设置说明](https://docs.crawlab.cn/Spider/ScrapySpider.html)
- 建议使用 scrapy 爬虫，此处以 tieba 爬虫为例，爬虫为标准 scrapy 文件结构
![](007_Crawlab爬虫管理平台/005_crawlab爬虫_tieba爬虫项目结构.png)
- 准备工作：
    - 确保 4.1 节中 crawlab 已经部署完成
    - 用户下面新建 crawlab 文件夹， 新建 yml 配置文件，具体参考 4.1.3 节
    - 将爬虫项目 tieba 文件夹复制到 /home/felix/crawlab 下面，和 yml 同级
    - 打开一个终端，切换到 crawlab 文件夹，执行以下命令启动 crawlab 容器
        - docker-compose up  确保 4 个服务启动成功
    - 再打开一个终端，切换到 /home/felix/crawlab/tieba 文件夹下
    ![](007_Crawlab爬虫管理平台/001_crawlab启动_上传本地爬虫项目到crawlab.png)
    - 执行以下命令，登陆 crawlab 爬虫管理平台，具体参考 4.1.4 节
        - crawlab login -u admin -a http://localhost:8080/api
    - 登陆成功后，执行以下命令上传项目到 crawlab 管理平台】
        - crawlab upload
    ![](007_Crawlab爬虫管理平台/004_CLI命令上传项目的crawlab管理平台.png)  
    - 上传成功后，浏览器打开 http://localhost:8080 自动跳转到管理界面，可以看到已经成功上传的爬虫
    ![](007_Crawlab爬虫管理平台/006_crawlab爬虫管理平台网页界面1.png)
    ![](007_Crawlab爬虫管理平台/007_crawlab爬虫管理平台网页界面2.png)
    - 停止docker-compose 容器，关闭 crawlab 管理平台
        - docker-compose down       停止并删除所有的容器 (推荐使用)
        - 因为容器镜像占用资源少，每次用完可以直接删除，下次重新启动一个全新的容器
    
    - 上面上传成功后，关闭删除后重新启动 容器 和上传项目
    - crawlab upload -n tb -N tieba_spider
    ![](007_Crawlab爬虫管理平台/008_停止删除crawlab镜像后_再次启动上传爬虫.png)
    - 点击爬虫名称，进入爬虫详情，对爬虫进行修改，修改后保存(灰色的不可修改，上传爬虫时候指定了爬虫名称，以该名称已经创建了代码目录)
    ![](007_Crawlab爬虫管理平台/009_crawlab爬虫管理平台_准备运行爬虫.png)
    - 点击右下方，运行爬虫，然后弹出窗口，确认就开始启动爬虫了
    ![](007_Crawlab爬虫管理平台/010_crawlab爬虫管理平台_启动爬虫1.png)
    ![](007_Crawlab爬虫管理平台/011_crawlab爬虫管理平台_启动爬虫2.png)
    - 运行中或者运行结束后，点击爬虫任务状态下面的进行中或者已完成查看任务详情
    - 任务详情里面有概览、日志(和WIN10启动爬虫后终端显示的日志结果一样)、结果
    ![](007_Crawlab爬虫管理平台/012_crawlab爬虫管理平台_爬虫运行结果查看1.png)
    ![](007_Crawlab爬虫管理平台/013_crawlab爬虫管理平台_爬虫运行结果查看_概览_日志_爬取结果.png)
    
    

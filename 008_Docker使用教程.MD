#### Docker使用教程
- [Docker中文文档-从入门到实践(详细全面)](https://yeasy.gitbooks.io/docker_practice/image/pull.html)
- [Docker菜鸟教程(简单实用，配有截图)](https://www.runoob.com/docker/docker-tutorial.html)
- [Docker 命令大全](https://www.runoob.com/docker/docker-command-manual.html)

# 1 Docker原理
- 对 Docker 最简单并且带有一定错误的认知就是 “Docker 是一种性能非常好的虚拟机”。
    - 正如上面所说，这是有一定错误的说法。Docker 相比于传统虚拟机的技术来说先进了不少，
    - 具体表现在 Docker 不是在宿主机上虚拟出一套硬件(VMare VBox虚拟机都是需要虚拟硬件，需要占用内存和硬盘)后再虚拟出一个操作系统，
    - 而是让 Docker 容器里面的进程直接运行在宿主机上（Docker 会做文件、网络等的隔离），
    - 这样一来 Docker 会 “体积更轻、跑的更快、同宿主机下可创建的个数更多”。

- Docker 中有三个核心概念：Image、Container、Repository。
    - Image 镜像： 
        - 有领“好人卡”倾向的广大程序猿一定对 镜像 的概念不会陌生。
        - 但和 windows 的那种 iso 镜像相比，Docker 中的镜像是分层的，可复用的，
        - 而非简单的一堆文件迭在一起（类似于一个压缩包的源码和一个 git 仓库的区别）。
    - Container 容器： 
        - 容器的存在离不开镜像的支持，他是镜像运行时的一个载体（类似于实例和类的关系）。
        - 依托 Docker 的虚拟化技术，给容器创建了独立的端口、进程、文件等“空间”，
        - Container 就是一个与宿机隔离 “容器”。容器可宿主机之间可以进行 port、volumes、network 等的通信。
        - 容器存储层的生存周期和容器一样，容器消亡时，容器存储层也随之消亡。因此，任何保存于容器存储层的信息都会随容器删除而丢失。
        - 数据卷的生存周期独立于容器，容器消亡，数据卷不会消亡。因此，使用数据卷后，容器删除或者重新运行之后，数据却不会丢失。
    - Repository 仓库： 
        - Docker 的仓库和 git 的仓库比较相似，拥有仓库名、tag。
        - 在本地构建完镜像之后，即可通过仓库进行镜像的分发。
        - 常用的 Docker hub 有 https://hub.docker.com/ 、 https://cr.console.aliyun.com/ 等。
        - 以 Ubuntu 镜像 为例，ubuntu 是仓库的名字，其内包含有不同的版本标签，如，16.04, 18.04。
        - 我们可以通过 ubuntu:16.04，或者 ubuntu:18.04 来具体指定所需哪个版本的镜像。如果忽略了标签，比如 ubuntu，那将视为 ubuntu:latest。
        - 仓库名经常以 两段式路径 形式出现，比如 jwilder/nginx-proxy，前者往往意味着 Docker Registry 多用户环境下的用户名，后者则往往是对应的软件名。
    
    - 镜像（Image）和容器（Container）的关系，就像是面向对象程序设计中的 类 和 实例 一样，
    - 镜像是静态的定义，容器是镜像运行时的实体。容器可以被创建、启动、停止、删除、暂停等。
    

# 2 Docker安装
- Ubuntu虚拟机中安装docker：docker-ce docker-ce-cli docker-compose
    - 具体安装步骤参考：[Ubuntu18.04 安装及使用Docker（安装常见报错及Docker常用命令）](https://blog.csdn.net/u011318077/article/details/104733149)
- docker全部安装完成后，镜像源修改中国的加速源地址，终端执行命令创建 sudo vi /etc/docker/daemon.json 文件，在其中输入如下内容。
   
        {
          "registry-mirrors": ["https://registry.docker-cn.com"]
        }
 
    - 然后输入:符号，输入wq保存退出
    
- Ubuntu安装使用Docker注意：
    - Docker安装完成后，如果不修改源，网速不好，有时候启动或者执行命令会出现失败或者超时提示
    - 安装博文中提到卸载后重新安装，后面发现是网速问题，只需要新建daemon.json文件，添加中国源即可
    - 注意，有些命令需要使用sudo docker xxx xxx ... 执行，直接docker执行会报错
    - 也可以将终端使用 su 回车 输入超级用户密码 回车 进入超级用户 显示符号位#
    
- Docker拖取镜像速度慢的终极解决办法：
    - 上面daemon.json虽然添加了官方的加速源地址，电信速度还可以(有时也很慢)，但是移动速度很慢，有时候超时或者失败
    - 推荐使用阿里云镜像，具体方法参考博文，[docker下载镜像使用阿里云加速器](https://blog.csdn.net/weixin_43569697/article/details/89279225?depth_1-utm_source=distribute.pc_relevant.none-task&utm_source=distribute.pc_relevant.none-task
)：
    - 具体步骤：
        - 1. 注册阿里云账号，搜索容器镜像服务，然后进入
        - 2. 镜像仓库里面新建一个镜像仓库
        - 3. 左侧菜单栏有个镜像加速器，点开
        - 4. 复制里面加速器地址，到daemon.json文件替换https://registry.docker-cn.com，保存退出
        - 5. 依次执行命令：
            - sudo systemctl daemon-reload    重载daemon.json配置文件
            - sudo systemctl restart docker   重启docker服务
        - 此时下载速度已经可以达到你的宽带速度正常值，可以删除一个镜像，然后重新下载对比速度。
        

- Docker安装注意事项:
    - Docker桌面版，WIN10系统只能专业版和企业版可以安装
    - 家庭版安装比较麻烦，需要视同toolbox工具或者修改注册表伪装为专业版骗过软件安装时候的检测
    - Docker安装在WIN10下面需要开启HyperV虚拟功能，该功能开启后会导致VMware和VirtualBox出错
    - 鉴于以上原因，不推荐在WIN10安装Docker,建议Ubuntu虚拟机服务器中安装
    - Win10安装可以具体参考我的QQ浏览器收藏夹中，python相关软件安装/docker安装，里面有家庭版和专业版安装收藏
    
# 3 镜像（Image）
## 3.1 获取镜像
- Docker Hub 上有大量的高质量的镜像可以用，这里我们就说一下怎么获取这些镜像。
    - 从 Docker 镜像仓库获取镜像的命令是 docker pull。其命令格式为：
    
    docker pull [选项] [Docker Registry 地址[:端口号]/]仓库名[:标签]
    
    - 具体的选项可以通过 docker pull --help 命令看到，这里我们说一下镜像名称的格式。
    - Docker 镜像仓库地址：地址的格式一般是 <域名/IP>[:端口号]。默认地址是 Docker Hub。
    - 仓库名：如之前所说，这里的仓库名是两段式名称，即 <用户名>/<软件名>。
    - 对于 Docker Hub，如果不给出用户名，则默认为 library，也就是官方镜像。
    - 比如：
        - docker pull ubuntu:18.04                  
            - 上面的命令中没有给出 Docker 镜像仓库地址，因此将会从 Docker Hub 获取镜像，省略了官方用户名 library
            - 而镜像名称是 ubuntu:18.04 实际将会获取官方镜像 library/ubuntu 仓库源中获取标签为 18.04 的镜像
        - docker pull httpd  不指定版本，默认获取latest
        - docker pull tikazyq/crawlab:latest        
            - 从DockerHub官方中的tikazyq用户获取crawlab镜像，版本为最新的latest 
        - docker pull registry.cn-hangzhou.aliyuncs.com/crawlab-team/crawlab:latest
            - 镜像地址：registry.cn-hangzhou.aliyuncs.com
            - 仓库名：用户名/软件名
                - 用户名：crawlab-team
                - 软件名：crawlab
                - 标签：latest
                - 从下载过程中可以看到我们之前提及的分层存储的概念，镜像是由多层存储所构成。
                - 下载也是一层层的去下载，并非单一文件。下载过程中给出了每一层的 ID 的前 12 位。
                - 并且下载结束后，给出该镜像完整的 sha256 的摘要，以确保下载一致性。
    - 镜像获取完成后，执行 docker images 即可看到本地所有的镜像
    [Docker获取镜像](008_Docker容器/001_Docker获取镜像.png)
    
- 运行一个简单的容器，以ubuntu:18.04为基础镜像
    - docker run -it --rm ubuntu:18.04 /bin/bash
    - docker run 就是运行容器的命令，具体格式我们会在 容器 一节进行详细讲解，我们这里简要的说明一下上面用到的参数。
    - 参数 -it 实际是两个参数，一个是 -i：交互式操作，一个是 -t 终端。我们这里打算进入 bash 执行一些命令并查看返回结果，因此我们需要交互式终端。
    - 参数 --rm 这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 docker rm。
        - 我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用 --rm 可以避免浪费空间。
    - 参数 ubuntu:18.04 这是指用 ubuntu:18.04 镜像为基础来启动容器。
    - 参数 /bin/bash 放在镜像名后的是 命令，这里我们希望有个交互式 Shell 终端，因此用的是 bash
    - 改命令执行以后，就启动了一个ubuntu系统下的shell终端，然后我们可以终端操作
        - cat /etc/os-release    查看当前容器镜像系统版本信息，cat命令就是打开查看文件信息
        - ls                     查看当前根目录下有哪些文件夹及文件
        - [以Ubuntu镜像运行一个容器](008_Docker容器/002_以Ubuntu镜像运行一个容器.png)
    - 最后我们通过 exit 命令退出了这个容器
    
## 3.2 查找拖取镜像
- 查找镜像
    - Docker Hub 网站来搜索镜像，Docker Hub 网址为： https://hub.docker.com/  直接访问网速不好
    - docker search 命令来搜索镜像。比如我们需要一个 httpd 的镜像来作为我们的 web 服务
    - 比如我们需要一个 httpd 的镜像来作为我们的 web 服务。我们可以通过 docker search 命令搜索 httpd 来寻找适合我们的镜像。
    - docker search httpd 
- 拖去镜像（参考上面3.1）
    - docker pull httpd  

## 3.3 列出镜像 
- 列出镜像
    - 以下两个命令都可以
        - docker image ls
        - docker images 
    - 镜像按CREATED,即创建时间排列，最近创建的在最上面
    - 列表包含了 仓库名、标签、镜像 ID、创建时间 以及 所占用的空间
    - 镜像 ID 则是镜像的唯一标识，一个镜像可以对应多个 标签， 因为标签相当于版本号，一个Ubuntu就有多个版本
- 列出镜像各个选项说明:
    - REPOSITORY：表示镜像的仓库源（类似软件名称）
    - TAG：镜像的标签 （类似软件版本号）
    - IMAGE ID：镜像ID
    - CREATED：镜像创建时间
    - SIZE：镜像大小

- 同一仓库源可以有多个 TAG，代表这个仓库源的不同个版本，如 ubuntu 仓库源里，有 15.10、14.04 等多个不同的版本，
    - 我们使用 REPOSITORY:TAG 来定义同一个仓库源中不同的镜像。
    
- 镜像体积
    - docker image ls 显示的是镜像下载到本地后，展开的大小，准确说，是展开后的各层所占空间的总和，
    - 因为镜像到本地后，查看空间的时候，更关心的是本地磁盘空间占用的大小，在Docker Hub上是压缩后的体积
    - 另外一个需要注意的问题是，docker image ls 列表中的镜像体积总和并非是所有镜像实际硬盘消耗。
    - 由于 Docker 镜像是多层存储结构，并且可以继承、复用，因此不同镜像可能会因为使用相同的基础镜像，
    - 从而拥有共同的层。由于 Docker 使用 Union FS，相同的层只需要保存一份即可，
    - 因此实际镜像硬盘占用空间很可能要比这个列表镜像大小的总和要小的多。
    - 以下命令来便捷的查看镜像、容器、数据卷所占用的空间
        - docker system df
    - [镜像列表展示](008_Docker容器/003_镜像列表展示.png)    

- 虚悬镜像
    - 一个特殊的镜像，这个镜像既没有仓库名，也没有标签，均为 <none>
    - docker pull 可能导致这种情况，docker build 也同样可以导致这种现象。
    - 由于新旧镜像同名，旧镜像名称被取消，从而出现仓库名、标签均为 <none> 的镜像。
    - 这类无标签镜像也被称为 虚悬镜像(dangling image)
    - 使用以下命令可以查看：
        - docker image ls -f dangling=true
    - 虚悬镜像已经失去了存在的价值，是可以随意删除的，可以用下面的命令删除虚悬镜像。
        - docker image prune
        
- 中间层镜像
    - 为了加速镜像构建、重复利用资源，Docker 会利用 中间层镜像。
    - 所以在使用一段时间后，可能会看到一些依赖的中间层镜像。
    - 默认的 docker image ls 列表中只会显示顶层镜像，如果希望显示包括中间层镜像在内的所有镜像的话，需要加 -a 参数。
        - docker image ls -a
    
- 列出部分镜像
    - docker image ls ubuntu                  列出标签名为ubuntu的所有镜像
    - docker image ls ubuntu:18.04            列表指定的镜像，指定仓库名和标签
    - docker image ls -f since=mongo:3.2      -f 就是filter过滤参数，列出mongo:3.2之后的镜像
    - docker image ls -f before=mongo:3.2     列出mongo:3.2之前的镜像
    
- 特定格式显示镜像列表
    - 只包含镜像ID和仓库名
    - docker image ls --format "{{.ID}}: {{.Repository}}"
    
        5f515359c7f8: redis
        05a60462f8ba: nginx
        fe9198c04d62: mongo
        00285df0df87: <none>
        1e0c3dd64ccd: ubuntu 
    
    - 以表格等距显示，并且有标题行，和默认一样，不过自己定义列
    - docker image ls --format "table {{.ID}}\t{{.Repository}}\t{{.Tag}}"
        
        IMAGE ID            REPOSITORY          TAG
        5f515359c7f8        redis               latest
        05a60462f8ba        nginx               latest         
        
## 3.4 删除镜像
- 删除本地的镜像，可以使用 docker image rm 命令，其格式为：
    - docker image rm [选项] <镜像1> [<镜像2> ...]
    - <镜像> 可以是 镜像短 ID、镜像长 ID、镜像名 或者 镜像摘要
        - 镜像的完整 ID，也称为 长 ID，来删除镜像。
        - 使用脚本的时候可能会用长 ID，但是人工输入就太累了，所以更多的时候是用 短 ID 来删除镜像。
        - docker image ls 默认列出的就已经是短 ID 了，一般取前3个字符以上，只要足够区分于别的镜像就可以了
    - 删除示例：
        - docker image rm da3fadgad34l      以完整IMAGE ID删除，推荐使用
        - docker image rm 501               短ID，IMAGE ID 前三位
        - docker image rm centos            镜像REPOSITORY仓库名称
        - docker image rm centos:latest     镜像REPOSITORY仓库名和标签名
        - 也可以使用以下命令删除
            - docker rmi hello-world  删除hello-world镜像
    - 精确的是使用 镜像摘要 删除镜像。
        - 查看摘要命令：docker image ls --digests
        - 以摘要删除镜像，@后面就是摘要：
            - docker image rm node@sha256:b4f0e0bdeb578043c1ea6862f0d40cc4afe32a4a582f3be235a3b164422be228

- 删除ID相同的镜像，直接使用ID删除，系统不知道删除那个，需要使用仓库名和标签名删除
    - [](008_Docker容器/019_删除ID相同的镜像使用仓库名和标签名.png)    
    
- 批量删除镜像
    - 删除所有仓库名为 redis 的镜像：
        - docker image rm $(docker image ls -q redis)
    - 删除所有在 mongo:3.2 之前的镜像：
        - docker image rm $(docker image ls -q -f before=mongo:3.2)    

- 删除命令执行后会出现 Untagged 和 Deleted
    - 如果观察上面这几个命令的运行输出信息的话，你会注意到删除行为分为两类，一类是 Untagged，另一类是 Deleted。
    - 我们之前介绍过，镜像的唯一标识是其 ID 和摘要，而一个镜像可以有多个标签。
    - 因此当我们使用上面命令删除镜像的时候，实际上是在要求删除某个标签的镜像。
    - 所以首先需要做的是将满足我们要求的所有镜像标签都取消，这就是我们看到的 Untagged 的信息。
    - 因为一个镜像可以对应多个标签，因此当我们删除了所指定的标签后，可能还有别的标签指向了这个镜像，
    - 如果是这种情况，那么 Delete 行为就不会发生。
    
    - 所以并非所有的 docker image rm 都会产生删除镜像的行为，有可能仅仅是取消了某个标签而已。
    - 当该镜像所有的标签都被取消了，该镜像很可能会失去了存在的意义，因此会触发删除行为。
    - 镜像是多层存储结构，因此在删除的时候也是从上层向基础层方向依次进行判断删除。
    - 镜像的多层结构让镜像复用变得非常容易，因此很有可能某个其它镜像正依赖于当前镜像的某一层。
    - 这种情况，依旧不会触发删除该层的行为。直到没有任何层依赖当前层时，才会真实的删除当前层。
    - 这就是为什么，有时候会奇怪，为什么明明没有别的标签指向这个镜像，但是它还是存在的原因，
    - 也是为什么有时候会发现所删除的层数和自己 docker pull 看到的层数不一样的原因。

    - 除了镜像依赖以外，还需要注意的是容器对镜像的依赖。
    - 如果有用这个镜像启动的容器存在（即使容器没有运行），那么同样不可以删除这个镜像。
    - 之前讲过，容器是以镜像为基础，再加一层容器存储层，组成这样的多层存储结构去运行的。
    - 因此该镜像如果被这个容器所依赖的，那么删除必然会导致故障。如果这些容器是不需要的，应该先将它们删除，然后再来删除镜像。 
    
 ## 3.5 创建的镜像
- 创建镜像的两种方式：
    - 更新镜像：从已经创建的容器中更新镜像，并且提交这个镜像
    - 构建镜像：使用 Dockerfile 指令来创建一个全新的镜像   

- 更新镜像：
    - 更新镜像之前，我们需要使用镜像来创建一个容器。比如：
        - runoob@runoob:~$ docker run -t -i ubuntu:15.10 /bin/bash
        - root@e218edb10161:/# 
    - 在运行的容器内使用 apt-get update 命令进行更新。
    - 在完成操作(比如在容器下安装一些包之类)之后，输入 exit 命令来退出这个容器。
    - 此时 ID 为 e218edb10161 的容器，是按我们的需求更改的容器。我们可以通过命令 docker commit 来提交容器副本。
    - 提交镜像就相当于添加了标签
        - runoob@runoob:~$ docker commit -m="has update" -a="runoob" e218edb10161 runoob/ubuntu:v2
        - sha256:70bf1840fd7c0d2d8ef0a42a817eb29f854c1af8f7c59fc03ac7bdee9545aff8
        - 各个参数说明：
            - -m: 提交的描述信息
            - -a: 指定镜像作者
            - e218edb10161：容器 ID
            - runoob/ubuntu:v2: 指定要创建的目标镜像名称，我们创建镜像时候要使用自己的账户名，felixzfb/ubuntu:v2
            - ubuntu镜像通过tag进行区别，上面tag就是v2
            - 一个镜像，不做修改，直接tag添加标签，新的镜像和原始镜像的ID是一样的
    - 特别注意：
        - commit 提交时候，软件名称斜线前面的用户名要写自己dockerhub的账户名，不然push到个人仓库会找不到用户名，会被denied
        - tag 标签时候，用户名也是自己的账户名，后面是仓库名称和tag标签
        - tag 标签命令可以用来修改镜像的 REPOSITORY 名称，也可以同时修改名称和tag
    - 详细细节参考5.2节更新镜像实例 
            
- 构建镜像：
    - 首先需要创建一个 Dockerfile 文件，其中包含一组指令来告诉 Docker 如何构建我们的镜像。
    - 比如构建一个
        - cat Dockerfile 
        - docker build -t runoob/centos:6.7 .
        - 参数说明：
            - -t ：指定要创建的目标镜像名
            - . ：Dockerfile 文件所在目录，可以指定Dockerfile 的绝对路径
    - 设置镜像标签
        - 我们可以使用 docker tag 命令，为镜像（可用镜像ID或者REPOSITORY名称）添加一个新的标签(REPOSITORY名称和TAG)。
        - runoob@runoob:~$ docker tag 860c279d2fec runoob/centos:dev



                     
  
# 4 容器（Container）
- 容器是独立运行的一个或一组应用，以及它们的运行态环境，类似一个虚拟机。
- 对应的，虚拟机可以理解为模拟运行的一整套操作系统（提供了运行态环境和其他系统环境）和跑在上面的应用。

## 4.1 创建启动容器
- 启动容器有两种方式，一种是基于镜像新建一个容器并启动，另外一个是将在终止状态（stopped）的容器重新启动。
- 因为 Docker 的容器实在太轻量级了，很多时候用户都是随时删除和新创建容器。
- 新建容器时候一般不指定容器名称，名称都是自动创建的，容器互联时候指定名称，参考5.2节

- 方式1：新建并启动进入容器
    - 所需要的命令主要为 docker run
    - 下面的命令输出一个 “Hello World”，之后就自动终止容器。
        - docker run ubuntu:18.04 /bin/echo 'Hello world'
        - Hello world
    - 这跟在本地直接执行 /bin/echo 'hello world' 几乎感觉不出任何区别。
    
    - 下面的命令则启动一个 bash 终端，允许用户进行交互。
        - docker run -t -i ubuntu:18.04 /bin/bash
        - docker run -it ubuntu:18.04 /bin/bash     该方式推荐使用
        - docker run -it ubuntu /bin/bash           如果ubuntu不指定版本号，会默认实用latest
        - docker run -itd ubuntu:18.04 /bin/bash    容器后台运行，新建容器时候不进入容器    
        - root@af8bae53bdd3:/#
        - 参数说明：
            - -t 选项让Docker分配一个伪终端（pseudo-tty）并绑定到容器的标准输入上， 
            - -i 则让容器的标准输入保持打开
            - -d 容器后台运行，不进入容器(不直接调出终端，要进入容器使用docker exec -it 243c32535da7 /bin/bash)
            
        - 在交互模式下，用户可以通过所创建的终端来输入命令，例如
            - root@af8bae53bdd3:/# pwd
            - /
            - root@af8bae53bdd3:/# ls
            - bin boot dev etc home lib lib64 media mnt opt proc root run sbin srv sys tmp usr var
        - exit 命令退出容器
        - docker container ls  查看容器信息，里面是空的
        - [新建启动容器](008_Docker容器/004_新建启动容器.png)
    
    - 当利用 docker run 来创建容器时，Docker 在后台运行的标准操作包括：
        - 检查本地是否存在指定的镜像，不存在就从公有仓库下载
        - 利用镜像创建并启动一个容器
        - 分配一个文件系统，并在只读的镜像层外面挂载一层可读写层
        - 从宿主主机配置的网桥接口中桥接一个虚拟接口到容器中去
        - 从地址池配置一个 ip 地址给容器
        - 执行用户指定的应用程序
        - 执行完毕后容器被终止  

- 方式2：新建启动容器(容器后台运行)
    - docker run -itd --name ubuntu-test ubuntu /bin/bash
    - 加了 -d 参数默认不会进入容器，想要进入容器需要使用指令 docker exec 命令，参考后面
    - docker ps      查看当前运行的容器所有信息
    - docker ps -a   查看已经终止的容器所有信息
    - 第一列是ID,最后一列是名称NAMES

- 方式3：启动已终止容器
    - 可以利用 docker start container_id 命令，直接将一个已经终止的容器启动运行。
    - 容器的核心为所执行的应用程序，所需要的资源都是应用程序运行所必需的。
    - 除此之外，并没有其它的资源。可以在伪终端中利用 ps 或 top 来查看进程信息。
        - root@ba267838cc1b:/# ps
            - PID TTY          TIME CMD
            - 1 ?        00:00:00 bash
            - 11 ?        00:00:00 ps
        - 可见，容器中仅运行了指定的 bash 应用。这种特点使得 Docker 对资源的利用率极高，是货真价实的轻量级虚拟化 
    - 再次启动已经终止的容器，启动后是在后台运行的
        - docker start container_id
        - 是在后台运行的，可以使用命令查看：docker container ls
        - docker stop container_id      终止容器
        - 再次docker container ls查看已经没有容器了
        - [启动已经终止的容器](008_Docker容器/005_启动已经终止的容器_停止后台运行的容器.png)
         
## 4.2 终止、重启容器
- docker stop container  来终止一个运行中的容器。
    - 此外，当 Docker 容器中指定的应用终结时，容器也自动终止。
    - 例如对于上一章节中只启动了一个终端的容器，用户通过 exit 命令或 Ctrl+d 来退出终端时，所创建的容器立刻终止。
    - 终止状态的容器可以用以下两个命令查看，结果相同：
        - docker container ls -a 
        - docker ps -a 
    - [终止容器](008_Docker容器/006_终止容器_查看已终止容器列表.png)  
- docker restart container_id  重新启动当前的容器 

## 4.3 进入后台容器
- 进入容器使用 -d 参数时，容器启动后会进入后台。此时想要进入容器，可以通过以下指令进入：
    - docker attach：不推荐使用，使用 exit 退出容器时，容器会自动终止
        - docker attach 243c32535da7
    - docker exec：推荐大家使用 docker exec 命令，因为此方法退出容器终端，不会导致容器的停止
        - docker exec -it 243c32535da7 /bin/bash
        
## 4.4 导出和导入容器
- docker export命令
    - docker export 7691a814370e > ubuntu.tar
    - 导出容器到本地文件
- docker import 从容器快照文件中再导入为镜像
    - cat ubuntu.tar | docker import - test/ubuntu:v1.0
    - test/ubuntu软件名称，v1.0为版本号
- 也可以通过指定 URL 或者某个目录来导入，例如
    - docker import http://example.com/exampleimage.tgz example/imagerepo  
    
## 4.5 删除容器
- 删除容器使用 docker rm 命令，删除容器是删除后台运行或者已终止的容器，因为容器id是唯一的
    - docker rm 容器名称或ID
    - docker rm -f 容器名称或ID
    - docker ps -a 查看已终止的容器
    - docker ps -l 查看最后一次创建的容器
    - 注意：删除容器时，容器必须是停止状态，否则会报如下错误
- 删除所有已终止的容器
    - docker container prune
    - [删除容器](008_Docker容器/007_新建容器删除容器删除所有容器.png) 
    
## 4.5 容器运行一个简单Web应用实例  
- docker容器中运行一个 Python Flask 应用来运行一个web应用      
1. 新建容器
    - docker pull training/webapp  # 载入镜像
    - docker run -d -P training/webapp python app.py
    - 参数说明:
        - -d:让容器在后台运行。
        - -P:将容器内部使用的网络端口映射到我们使用的主机上。
        - Docker 开放了 5000 端口（默认 Python Flask 端口）映射到主机端口 32768 上。
    - 通过主机的浏览器访问容器内部WEB应用：192.168.0.21:5000 
    - [创建Webapp应用](008_Docker容器/008_创建Webapp应用.png)
    
    - -p 指定映射端口
        - docker run -d -p 5000:5000 training/webapp python app.py
        - docker ps 查看容器列表信息，里面有端口PORTS的详细映射信息

- 2. 查看容器映射网络端口      
    - docker port container_name or container_id 可以查看容器端口的映射情况
        - 5000/tcp -> 0.0.0.0:5000   前面是容器端口，后面是映射的主机（0.0.0.0就是当前电脑主机）和端口
        
- 3. 查看Web应用程序日志
    - docker logs -f 容器名称或者ID
    - -f: 让 docker logs 像使用 tail -f 一样来输出容器内部的标准输出。 
    - 退出使用ctrl + z 或者 ctrl + d
    
- 4. 查看web应用程序的进程
    - docker top 容器名称或者ID 
    
- 5. 检查 WEB 应用程序
    - docker inspect 容器名称或者ID
    - 查看 Docker 的底层信息。它会返回一个 JSON 文件记录着 Docker 容器的配置和状态信息。
    - [](008_Docker容器/010_检查容器启动容器停止容器删除容器1.png)
    
- 6. 停止 WEB 应用容器
    - docker stop 容器名称或者ID
    
- 7. 重启WEB应用容器
    - 已经停止的容器，我们可以使用命令 docker start 来启动。
    - docker start 容器名称或者ID
    - [](008_Docker容器/011_检查容器启动容器停止容器删除容器2.png)
    
# 5 Docker 容器连接
## 5.1 网络端口映射
- 上面的4.5节中我们实现了通过网络端口来访问运行在 docker 容器内的服务。
- 容器中可以运行一些网络应用，要让外部也可以访问这些应用，可以通过 -P 或 -p 参数来指定端口映射。
    - -P : 是容器内部端口随机映射到主机的高端口。
    - -p : 是容器内部端口绑定到指定的主机端口。
    - 比如以下实例:
    - docker run -d -P training/webapp python app.py
        - PORTS： 0.0.0.0:32768->5000/tcp  容器应用的5000端口映射到主机上的32768端口
    - docker run -d -p 5000:5000 training/webapp python app.py
        - PORTS:  0.0.0.0:5000->5000/tcp   容器应用的5000端口映射到主机上指定的5000端口
        - 我们可以通过浏览器 192.168.0.21:5000 来访问容器的 5000 端口，即容器内部的web应用

- 可以指定容器绑定的网络地址，比如绑定 127.0.0.1
    - docker run -d -p 127.0.0.1:5001:5000 training/webapp python app.py
        - PORTS：127.0.0.1:5001->5000/tcp  容器应用的5000端口映射到网络IP地址127.0.0.1指定的5000端口
        - 我们可以通过浏览器 127.0.0.1:5001 来访问容器的 5000 端口，即容器内部的web应用

- 上述方法，默认绑定都是tcp端口
    - 如果要绑定udp端口，端口号后面加上/udp即可
    - docker run -d -p 127.0.0.1:5000:5000/udp training/webapp python app.py
        - PORTS：127.0.0.1:5000->5000/udp

- 查看容器映射网络端口      
    - docker port container_name or container_id 可以查看容器端口的映射情况  
    
## 5.2 Docker容器互联
- 端口映射并不是唯一把 docker 连接到另一个容器的方法。
    - docker 有一个连接系统允许将多个容器连接在一起，共享连接信息。
    - docker 连接会创建一个父子关系，其中父容器可以看到子容器的信息。
    
- 容器命名
    - 当我们创建一个容器的时候，docker 会自动对它进行命名。另外，我们也可以使用 --name 标识来命名容器，例如：
    - runoob@runoob:~$  docker run -d -P --name runoob training/webapp python app.py
    - 指定容器的名称为 runoob
    
- 新建网络
    - 下面先创建一个新的 Docker 网络。
    - docker network create -d bridge test-net
    - 参数说明：
        - -d：参数后面指定 Docker 网络类型，有 bridge、overlay。
        - 其中 overlay 网络类型用于 Swarm mode，在本小节中你可以忽略它。
        - test-net：网络的名称，后面容器连接该网络时候使用该名称
        - -d： 在前面创建容器时候，用途是新建容器后，容器后台运行，不进入容器
    - [](008_Docker容器/012_Docker容器互联_创建网络.png)

- 连接容器
    - 该终端运行一个容器并连接到上面新建的 test-net 网络:
        - docker run -itd --name test1 --network test-net ubuntu /bin/bash
    - 打开新的终端，再运行一个容器并加入到 test-net 网络:
        - docker run -itd --name test2 --network test-net ubuntu /bin/bash
    - 安装 ping 工具（网络连通测试）
        - 如果 test1、test2 容器内中无 ping 命令，则在容器内执行以下命令安装 ping
            - apt-get update                先更新以下源地址列表
            - apt install iputils-ping      下载安装 ping 工具

    - 具体步骤：
        - 进入test1的容器终端：docker exec -it test1 /bin/bash
        - 然后执行上面两个命令：
            - apt-get update
            - apt install iputils-ping
        - [](008_Docker容器/013_Docker容器互联_更新源地址列表然后安装ping.png)
    
    - 安装完成后，然后分别进行ping测试：
        - test1容器：ping test2
        - test2容器：ping test1
        - 连接成功，相互就有数据传输
        - [](008_Docker容器/014_Docker容器互联_容器相互ping测试.png)

- 更新镜像实例： 
    - 上面我们已经在一个容器里面，更新了源地址列表，同时又安装了ping工具
    - 此时镜像和创建容器时候的镜像已经发生了改变，我们可以提交为自己的镜像
    - 下次创建容器时候就可以用我们自己的镜像，里面的包就不用重新安装了  
    - 上面已经更新了Ubuntu的源列表，并安装了ping工具，先 exit 命令退出容器，我们提交容器副本：
        - docker commit -m="has update" -a="felix" e218edb10161 felix/ubuntu:v2
        - 各个参数说明：
            - -m: 提交的描述信息
            - -a: 指定镜像作者，即用户名
            - e218edb10161：容器 ID
            - felixzfb/ubuntu:v2: 指定要创建的目标镜像名称 (REPOSITORY仓库名)和版本号（TAG）
            - ubuntu不同的镜像通过tag的v2进行区分
            - 提交的镜像就已经有了新的tag标签
        - 提交后本地镜像库就有了刚刚提交的镜像，提交成功如下图：
        - [](008_Docker容器/015_更新镜像_提交容器副本_更新本地镜像.png)

## 5.3 Docker Hub 个人仓库管理
- 在 https://hub.docker.com 免费注册一个 Docker 账号 
    - 网速很慢，需要挂代理，注册后选择免费community版
    - 本地登录和退出用户
        - docker login
        - docker logout
        - 登录需要输入用户名和密码，登录成功后，我们就可以从 docker hub 上拉取自己账号下的全部镜像
        - 登陆用户时候不用挂代理，因为daemon.json已经设置了阿里云加速地址，但是有时网速不好会登陆不上
    - 推送镜像
        - 用户登录后，可以通过 docker push 命令将自己的镜像推送到 Docker Hub。
        - docker tag ubuntu:18.04 felixzfb/ubuntu:18.04  将本地的ubuntu:18.04镜像直接使用添加tag标签变成自己镜像
        ```
            REPOSITORY      TAG        IMAGE ID            CREATED           ...  
            ubuntu          18.04      275d79972a86        6 days ago        ...  
            felixzfb/ubuntu 18.04      275d79972a86        6 days ago
        ```
        - 上述添加标签的镜像ID相同，因为直接用的本地镜像添加标签，未做任何改动，ID一模一样
        - 参考015图片，本地镜像进行更新提交后的镜像，是一个全新的镜像ID已经发生了变化
        - docker push felixzfb/ubuntu:18.04  将添加标签的镜像推送到Docker Hub自己的账户中，即felixzfb中
        - docker search felixzfb/ubuntu      搜索自己仓库的镜像
        - 特别注意：
            - commit 提交时候，软件名称斜线前面的用户名要写自己dockerhub的账户名，不然push到个人仓库会找不到用户名，会被denied
            - tag 标签时候，用户名也是自己的账户名，后面是仓库名称和tag标签
            - tag 标签命令可以用来修改镜像的 REPOSITORY 名称，也可以同时修改名称和tag
        - [](008_Docker容器/016_登陆个人仓库_上传本地镜像到个人仓库.png)
        - [](008_Docker容器/017_登陆个人仓库_上传本地自己的镜像到个人仓库.png)
        - [](008_Docker容器/018_登陆个人网站_查看已上传的镜像.png)
        - 上述图片可以发现：
            - docker push felix/ubuntu  失败，因为它去查找的是felix账户，不是自己的账户，没有权限
            - 然后将felix/ubuntu 镜像直接使用 tag 命令修改，相当于修改 REPOSITORY 名称得到的镜像和原始镜像的ID是一模一样的

- 删除ID相同的镜像，直接使用ID删除，系统不知道删除那个，需要使用仓库名和标签名删除
    - [](008_Docker容器/019_删除ID相同的镜像使用仓库名和标签名.png)
            

## 5.4 配置全部容器的DNS
- 我们可以在宿主机的 /etc/docker/daemon.json 文件中增加以下内容来设置全部容器的 DNS：
        ```
        {
          "dns" : [
            "114.114.114.114",
            "8.8.8.8"
          ]
        }
        ```
- 设置后，启动容器的 DNS 会自动配置为 114.114.114.114 和 8.8.8.8。
    - 配置完，需要重启 docker 才能生效: 
        - /etc/init.d/docker restart
    - 查看容器的 DNS 是否生效可以使用以下命令:
        - docker run -it --rm ubuntu  cat etc/resolv.conf
        - 它会输出容器的 DNS 信息:
            - nameserver 114.114.114.114
            - nameserver 8.8.8.8
            
            
- 手动指定单个容器的配置
    - 如果只想在指定的容器设置 DNS，则可以使用以下命令：
    - docker run -it --rm -h host_ubuntu --dns=114.114.114.114 --dns-search=test.com ubuntu
    - 参数说明：
        - -h HOSTNAME 或者 --hostname=HOSTNAME： 设定容器的主机名，它会被写到容器内的 /etc/hostname 和 /etc/hosts。可以通过，cat /etc/hostname 查看文件内容 
        - --dns=IP_ADDRESS： 添加 DNS 服务器到容器的 /etc/resolv.conf 中，让容器用这个服务器来解析所有不在 /etc/hosts 中的主机名。    
        - --dns-search=DOMAIN： 设定容器的搜索域，当设定搜索域为 .example.com 时，在搜索一个名为 host 的主机时，DNS 不仅搜索 host，还会搜索 host.example.com。        
    - 如果在容器启动时没有指定 --dns 和 --dns-search，Docker 会默认用宿主主机上的 /etc/resolv.conf 来配置容器的 DNS    
     
# 6 Docker Compose
## 6.1  Compose 简介
- Compose 是用于定义和运行多容器 Docker 应用程序的工具。
- 通过 Compose，您可以使用 YML 文件来配置应用程序需要的所有服务。
- 然后，使用一个命令，就可以从 YML 文件配置中创建并启动所有服务。
- Compose 使用的三个步骤：
    - 使用 Dockerfile 定义应用程序的环境。
    - 使用 docker-compose.yml 定义构成应用程序的服务，这样它们可以在隔离环境中一起运行。
    - 最后，执行 docker-compose up 命令来启动并运行整个应用程序 
- docker-compose安装 第 2 章里面的博文，安装完成后输入，docker-compose --version 显示版本就是安装成功

- docker-compose使用需要配置 yml 文件，yml 文件配置说明参考以下文章
- [YAML 入门教程](https://www.runoob.com/w3cnote/yaml-intro.html)

## 6.2 docker-compose 使用案例
- 配置文件尽量粘贴复制，以防出错
- 由于我的Ubuntu和Win之间出现相互之间不能粘贴复制，但是共享文件夹可以访问
- 折中办法：共享文件夹中新建打开一个txt文件，WIN10下面复制粘贴，Ubuntu每次重新载入，相当于一个实时剪贴板

- 1. 准备
    - 创建一个测试目录：
        - mkdir composetest  
        - cd composetest
        - touch app.py       测试目录中创建一个名为 app.py 的文件
        - 具体步骤如下图，具体文件内部内容都是WIN10直接复制到txt剪贴板，然后粘贴进去
        
        -示例中，redis 是应用程序网络上的 redis 容器的主机名，该主机使用的端口为 6379。
        - 然后继续在 composetest 目录中创建另一个名为 requirements.txt 的文件，内容参考截图
         
    - [](008_Docker容器/020_docker-compose使用准备.png)
    
- 2. 创建 Dockerfile 文件
    - 在 composetest 目录中，创建一个名为的文件 Dockerfile
    - 具体内容如下截图
    - Dockerfile 内容解释：
        - FROM python:3.7-alpine: 从 Python 3.7 映像开始构建镜像。
        - WORKDIR /code: 将工作目录设置为 /code。
        - ENV FLASK_APP app.py
        - ENV FLASK_RUN_HOST 0.0.0.0
        - 设置 flask 命令使用的环境变量。
        
        - RUN apk add --no-cache gcc musl-dev linux-headers
        - 安装 gcc，以便诸如 MarkupSafe 和 SQLAlchemy 之类的 Python 包可以编译加速。
        - COPY requirements.txt requirements.txt
        - RUN pip install -r requirements.txt
        - 复制 requirements.txt 并安装 Python 依赖项。
        
        - COPY . .: 将 . 项目中的当前目录复制到 . 镜像中的工作目录。
        - CMD ["flask", "run"]: 容器提供默认的执行命令为：flask run。
    - [](008_Docker容器/021_docker-compose使用_创建Dockerfile文件1.png)
    - [](008_Docker容器/022_docker-compose使用_创建Dockerfile文件2.png)
        
- 3. 创建 docker-compose.yml
    - 在测试目录中创建一个名为 docker-compose.yml 的文件
    - 该 yml 文件定义了两个服务：web 和 redis。
        - web：该 web 服务使用从 Dockerfile 当前目录中构建的镜像。然后，它将容器和主机绑定到暴露的端口 5000。此示例服务使用 Flask Web 服务器的默认端口 5000 。
        - redis：该 redis 服务使用 Docker Hub 的公共 Redis 映像。
    - [](008_Docker容器/023_docker-compose使用_创建docker-compose.yml配置文件.png)    
    
- 4. 使用 Compose 命令构建和运行您的应用
    - 在测试目录中，执行以下命令来启动应用程序：
        - docker-compose up
    - 如果你想在后台执行该服务可以加上 -d 参数：
        - docker-compose up -d
        
- 该实例及 yml 配置详细配置参考：[菜鸟教程-Docker Compose](https://www.runoob.com/docker/docker-compose.html)

    
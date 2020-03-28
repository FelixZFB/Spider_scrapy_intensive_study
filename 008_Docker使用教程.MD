#### Docker使用教程
- [Docker中文文档-从入门到实践](https://yeasy.gitbooks.io/docker_practice/image/pull.html)

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
            - 上面的命令中没有给出 Docker 镜像仓库地址，因此将会从 Docker Hub 获取镜像。
            - 而镜像名称是 ubuntu:18.04因此将会获取官方镜像 library/ubuntu 仓库中标签为 18.04 的镜像
        - docker pull tikazyq/crawlab:latest        
            - 从DockerHub中的tikazyq用户获取crawlab镜像，版本为最新的latest 
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
    - docker run -it --rm ubuntu:18.04 bash
    - docker run 就是运行容器的命令，具体格式我们会在 容器 一节进行详细讲解，我们这里简要的说明一下上面用到的参数。
    - 参数 -it 实际是两个参数，一个是 -i：交互式操作，一个是 -t 终端。我们这里打算进入 bash 执行一些命令并查看返回结果，因此我们需要交互式终端。
    - 参数 --rm 这个参数是说容器退出后随之将其删除。默认情况下，为了排障需求，退出的容器并不会立即删除，除非手动 docker rm。
        - 我们这里只是随便执行个命令，看看结果，不需要排障和保留结果，因此使用 --rm 可以避免浪费空间。
    - 参数 ubuntu:18.04 这是指用 ubuntu:18.04 镜像为基础来启动容器。
    - 参数 bash 放在镜像名后的是 命令，这里我们希望有个交互式 Shell 终端，因此用的是 bash
    - 改命令执行以后，就启动了一个ubuntu系统下的shell终端，然后我们可以终端操作
        - cat /etc/os-release    查看当前容器镜像系统版本信息，cat命令就是打开查看文件信息
        - ls                     查看当前根目录下有哪些文件夹及文件
        - [以Ubuntu镜像运行一个容器](008_Docker容器/002_以Ubuntu镜像运行一个容器.png)
    - 最后我们通过 exit 命令退出了这个容器
    
## 3.2 列出镜像 
- 列出镜像
    - 以下两个命令都可以
        - docker image ls
        - docker images 
    - 镜像按获取时间，最近获取的在最上面
    - 列表包含了 仓库名、标签、镜像 ID、创建时间 以及 所占用的空间
    - 镜像 ID 则是镜像的唯一标识，一个镜像可以对应多个 标签， 因为标签相当于版本号，一个Ubuntu就有多个版本
    
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
        
## 3.3 删除镜像
- 删除本地的镜像，可以使用 docker image rm 命令，其格式为：
    - docker image rm [选项] <镜像1> [<镜像2> ...]
    - <镜像> 可以是 镜像短 ID、镜像长 ID、镜像名 或者 镜像摘要
        - 镜像的完整 ID，也称为 长 ID，来删除镜像。
        - 使用脚本的时候可能会用长 ID，但是人工输入就太累了，所以更多的时候是用 短 ID 来删除镜像。
        - docker image ls 默认列出的就已经是短 ID 了，一般取前3个字符以上，只要足够区分于别的镜像就可以了
    - 删除示例：
        - docker image rm 501               短ID前三位
        - docker image rm centos            镜像REPOSITORY仓库名称
        - docker image rm centos:latest     镜像REPOSITORY仓库名和标签名
    - 精确的是使用 镜像摘要 删除镜像。
        - 查看摘要命令：docker image ls --digests
        - 以摘要删除镜像，@后面就是摘要：
            - docker image rm node@sha256:b4f0e0bdeb578043c1ea6862f0d40cc4afe32a4a582f3be235a3b164422be228

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
  
# 4 容器（Container）
- 容器是独立运行的一个或一组应用，以及它们的运行态环境，类似一个虚拟机。
- 对应的，虚拟机可以理解为模拟运行的一整套操作系统（提供了运行态环境和其他系统环境）和跑在上面的应用。
## 4.1 创建启动容器      
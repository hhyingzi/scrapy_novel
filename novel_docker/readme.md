# hhyingzi/novel_docker
## 安装环境与依赖
### 下载官方images依赖
```
# anaconda
$ docker pull continuumio/anaconda3

# selenium
$ docker pull selenium/standalone-chrome
```

#### 以服务形式运行 selenium
- 容器名：selenium
- 端口监听：4444

```
$ docker run -d -p 4444:4444 --shm-size="2g" --name selenium selenium/standalone-chrome

# Python代码可以这样连接 selenium 服务：
/*
driver = webdriver.Remote(
	command_executor='http://127.0.0.1:4444',
	desired_capabilities={'browserName': 'chrome'}
)
*/
```
运行后，在浏览器或python访问：http://127.0.0.1:4444 即可使用。

#### 使用 anaconda3 运行源代码，以 Executable 形式
- 容器名：novel
- 调用方法：$ docker start novel
- 卷名：novel
	- windows 绑定地址：D:\code\python\爬虫\novel\novel
	- Ubuntu 绑定地址：/home/code/python/novel/...
```
# 定义项目源码所在的卷 novel ，在 run 的时候将卷绑定到本地源码目录
$ docker volume create novel

# build 映像 hhyingzi/novel
$ docker build --tag hhyingzi/novel .

# run 起来，命名为 novel，并将卷绑定到本地源代码目录
$ docker run --network host --mount type=bind,src="D:\\code\\python\\爬虫\\novel\\novel",dst=/novel --name novel hhyingzi/novel

$ docker run --network host --mount type=bind,src=/home/code/python/novel/scrapy_novel/,dst=/novel --name novel hhyingzi/novel

$ docker start novel

$ docker start -it novel /bin/bash
```

# 源码地址
- Github: git@github.com:hhyingzi/scrapy_novel.git
- Gitee码云：git@gitee.com:hhyingzi/scrapy_novel.git
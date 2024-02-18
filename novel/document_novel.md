# Document of Novel Spider
## 数据来源
### 官方来源
- 起点 qidian.py
- 纵横中文网 zongheng.py

### 内容来源
- 天域小说网

## Database 数据库
### 数据库设计
#### 用户管理
- 数据库：admin

用户名 | 密码        | 权限 | 说明
--- |-----------| --- | ---
root | w******** | userAdminAnyDatabase | 管理用户
user1 | w********    | userAdminAnyDatabase, dbAdminAnyDatabase | 操作数据库，写入数据

#### 数据管理
##### novel，小说数据库
```
use novel

collection: overview，“总览”集合，根据起点网获取的信息
{
    "title" : 小说名
     "info": {
            "author": 作者
            "last_read_chapter": 上次阅读章节
            "last_chapter": 最新章节名
            "update_date": 更新日期和时间（爬取结果）
            "pretty_update_date": <num>小时前 字样
			"now":现在时间
        }
}

collection: detail，小说具体信息
{
    "title": 小说名
    {
        "site_name": 网站名称
         {
            "cata_url": 目录url
            "catalog": 小说目录, 
                {
                    "chapter_url": 章节url
                    "content": 文本内容
                    "timestamp": 录入时间戳
                 }
            "last_chapter": 最新章节名
            "hidden_index": 隐藏计数，辅助给目录排序，索引
         }
    }
}
```

## Web 设计
### 后端
- Spring Boot DevTools：修改源代码后自动刷新内容
- Lombok：自动生成 get set 方法
- Spring Web：MVC
- Tyhmeleaf：对象-html数据接口
- Spring Data MongoDB：连接MongoDB数据库
- Rest Repositories：使用Rest风格

警告：
- spring-data-jpa：使用jpa风格，会与MongoDB数据库冲突

### 前端
无

## 语言参考
### log 输出
```angular2html
from logging import getLogger

logger = getLogger()
logger.debug('Hello')
```

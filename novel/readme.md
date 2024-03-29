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
user1 | w******** | userAdminAnyDatabase, dbAdminAnyDatabase | 操作数据库，写入数据

#### 数据管理
##### novel info 数据库
##### content 数据库

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

# 开发计划
## 已完成：提供小说主页URL，拉取小说详细信息，存入 MongoDB。
## 已完成：从小说主页，跳转目录页，拉取小说各章节标题和URL
## 已完成：根据小说各章节的URL，拉取章节内容，存入 MongoDB。

## 待开发：根据小说名称，删除 novel_info 和 content 数据
需求：根据小说名称，彻底删除这个小说。
原因：
- 主要用于小说内容有问题，重新拉取。
- 增量拉取或修改拉取功能尚未开发，所以先用这个功能垫着。

输入：小说名称。
行为：
- 首先根据章节列表，删除 content 中所有章节。
- 然后删除 novel_info 数据项。

## 待开发：小说增量拉取
novel_info：
新增字段：last_update_chapter：章节名

- 新增的章节信息，更新至 novel_info 的“待爬取”字段。
- 爬取“待爬取”章节至 content。然后补充至 novel_info 的章节列表中。
- 计算最新章节，更新至 novel_info 的“最近更新”字段，如果没有则为空。

## 待开发：小说删除无效章节
新建字段：待删除章节列表“invalid_chapter_list”

从其他业务中，计算出“无效章节”列表，覆盖或更新至 novel_info 的待删除章节列表“invalid_chapter_list”

本任务专门处理该无效章节信息：
- 根据 novel_info.chapters 和 invalid_chapter_list ，计算出最新有效章节，更新至 novel_info 的最近章节 “last_chapter” 字段，如果没有则为空。
- 根据 novel_info.invalid_chapter_list， 从 content 中，删除“无效章节”。从 novel_info.chapter 中，删除“无效章节”

## 代开发：去重过滤器 filter

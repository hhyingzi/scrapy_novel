# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import datetime
import pytz

import configparser
import novel
import logging

# 天域小说网内容，存储到 MongoDB
class TianyuPipeline:
    def __init__(self):
        # 加载配置文件
        config = configparser.ConfigParser()
        config.read('mypass.ini')

        # 加载数据库配置
        self.mongo_host = config.get('mongodb', 'mongo_host')
        self.mongo_port = int(config.get('mongodb', 'mongo_port'))
        self.mongo_username = config.get('mongodb', 'mongo_username')
        self.mongo_password = config.get('mongodb', 'mongo_password')
        self.authSource = 'admin'  # 用于登录的数据库，需要指定为用户凭据所在位置
        self.db_novel = 'novel'  # 用于写入业务数据的数据库

        # 日志
        self.pipeline_logger = logging.getLogger("PipelineLogger")

    def open_spider(self, spider):
        # 建立数据库连接
        self.client = pymongo.MongoClient(host=self.mongo_host,
                                          port=self.mongo_port,
                                          username=self.mongo_username,
                                          password=self.mongo_password,
                                          authSource=self.authSource)
        # 指定 database: novel
        self.db = self.client[self.db_novel]
        # 指定 collection
        self.novel_info_collection = self.db['novel_info']  # novel_info 用于预览小说
        self.content_collection = self.db['content']  # content 用于存储小说具体章节

        # 验证数据库连接
        try:
            self.client.admin.command('ping')
            self.pipeline_logger.info("MongoDB connect successful.")
        except pymongo.errors.ConnectionFailure:
            self.pipeline_logger.error("Mongodb server not available! 服务器无法连接！")
            exit(1)
        except pymongo.errors.OperationFailure:
            self.pipeline_logger.error(f'Mongodb Authentication faild! 认证失败！ user:{self.mongo_username}, db:{self.authSource}')
            exit(1)

    def close_spider(self, spider):
        # 关闭数据库连接
        self.client.close()
        self.pipeline_logger.info("MongoDB connection closed.")

    def process_item(self, item, spider):
        try:
            if isinstance(item, novel.items.NovelItem):
                self.pipeline_logger.info("Is NovelItem")
                # 插入小说信息
                search_this_book = self.novel_info_collection.find_one(
                    {'title': item['title']},  # 根据item的小说名称，查询数据库数据
                    {  # 查询结果提供以下字段
                        'last_chapter': item['last_chapter'],  # 数据库中已有的最新章节。
                    }
                )
                # 数据库无该书名，则插入。
                if search_this_book is None:
                    self.novel_info_collection.insert_one(ItemAdapter(item).asdict())
                    self.pipeline_logger.info(f"小说信息已更新入数据库:{item["title"]}")
                # 否则，待新增其他逻辑：判断最新章节是否相同，是否有必要更新等。
                else:
                    # 要重新下载，需要遍历删除所有的已有章节
                    # 然后更新小说信息，包括所有章节
                    self.pipeline_logger.warning(f"小说信息未更新入数据库. Item 内容为：{item}")
                return item
            elif isinstance(item, novel.items.ChapterItem):
                self.pipeline_logger.info("Is ChapterItem")
                update_result = self.content_collection.update_one(
                    filter={
                        "book_name": item["book_name"],
                        "chapter_name": item["chapter_name"]
                    },
                    update={'$set': ItemAdapter(item).asdict()},
                    upsert=True
                )
                if update_result.upserted_id is not None:
                    self.pipeline_logger.info(f"章节内容已新增:{item["book_name"]}: {item["chapter_name"]}")
                elif update_result.matched_count != 1:
                    self.pipeline_logger.warning(f"章节数据出现冗余，只修改第一条:{item["book_name"]}: {item["chapter_name"]}")
                elif update_result.modified_count == 1:
                    self.pipeline_logger.info(f"章节内容已更新:{item["book_name"]}: {item["chapter_name"]}")
                elif update_result.modified_count == 0:
                    self.pipeline_logger.info(f"章节内容已是最新。:{item["book_name"]}: {item["chapter_name"]}")
                else:
                    self.pipeline_logger.error(f"章节内容更新时，数据出现未知错误:{item}")

                # chapter_existed = self.content_collection.find_one({"book_name": item["book_name"], "chapter_name": item["chapter_name"]})
                # if not chapter_existed:
                #     # 如果该章不存在，则直接插入
                #     self.content_collection.insert_one(ItemAdapter(item).asdict())
                #     self.pipeline_logger.info(f"章节内容已新增:{item["book_name"]}: {item["chapter_name"]}")
                # else:
                #     # 如果该章已存在，则更新
                #     self.content_collection.update_one({'book_name': item['book_name'], 'chapter_name': item['chapter_name']}, ItemAdapter(item).asdict())
                #     self.pipeline_logger.info(f"章节内容已更新:{item["book_name"]}: {item["chapter_name"]}")
                return item
            else:
                print(type(item) + " Not any recognised item.")
                raise BaseException
        except BaseException as e:
            self.pipeline_logger.log(logging.ERROR, f"小说信息更新异常。{str(e)}")
            raise e


# class QidianPipeline:
#     def __init__(self):
#         config = configparser.ConfigParser()
#         config.read('mypass.ini')
#
#         self.mongo_host = config.get('mongodb', 'mongo_host')
#         self.mongo_port = int(config.get('mongodb', 'mongo_port'))
#         self.mongo_username = config.get('mongodb', 'mongo_username')
#         self.mongo_password = config.get('mongodb', 'mongo_password')
#         self.authSource = 'admin'  # 用于登录的数据库，需要指定为用户凭据所在位置
#         self.db_novel = 'novel'  # 用于写入业务数据的数据库
#         self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port, username=self.mongo_username,
#                                           password=self.mongo_password, authSource=self.authSource)
#
#         self.db = self.client[self.db_novel]  # database: novel
#         self.overview = self.db['overview']  # collection: overview
#         self.detail = self.db['detail']  # collection: detail
#
#     def open_spider(self, spider):
#         try:
#             self.client.admin.command('ping')
#         except pymongo.errors.ConnectionFailure:
#             print("Mongodb server not available! 服务器无法连接！")
#             exit(1)
#         except pymongo.errors.OperationFailure:
#             print('Authentication faild: user:user1, db:db_test')
#             exit(1)
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#
#         # 查询数据库中，该小说的“最近已读章节”和“更新日期”
#         queried = self.overview.find_one({'title': item['title']},
#                                          {
#                                              'info.last_read_chapter': 1,  # 数据库中的最近已读章节
#                                              'info.update_date': 1  # 数据库中的最近更新日期
#                                          })
#         # 提取出上述字段。
#         if queried is not None:
#             if 'last_read_chapter' not in queried['info']:
#                 queried_last_read_chapter = None
#                 queried_update = queried['info']['update_date']
#             else:
#                 queried_last_read_chapter = queried['info']['last_read_chapter']
#                 queried_update = queried['info']['update_date']
#         # 数据库没有该字段。
#         else:
#             queried_last_read_chapter = None
#             queried_update = None
#
#         # 推送数据的格式
#         # db_post_test = ItemAdapter(item).asdict()
#         db_post = {
#             'title': item['title'],
#             'info': {
#                 "author": item['author'],
#                 "last_read_chapter": queried_last_read_chapter,
#                 "last_chapter": item['last_chapter'],
#                 "update_date": item['update_date'],
#                 "pretty_update_date": item['pretty_update_date'],
#                 "now": datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
#             }
#         }
#
#         # 数据库无该书条目则插入，有该书但不是最新则修改 info{'last_chapter', 'update_date', 'pretty_update_date'}, ，否则不做操作
#         if queried is None:
#             self.overview.insert(db_post)
#             self.logger.debug(db_post)
#             return item
#         elif queried_update != item['update_date']:
#             self.overview.update_one(
#                 {'title': item['title']},
#                 {'$set': {
#                     'info': {
#                         "author": item['author'],
#                         "last_chapter": item['last_chapter'],
#                         "update_date": item['update_date'],
#                         "pretty_update_date": item['pretty_update_date'],
#                         "now": datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
#                     }
#                 }}, upsert=True
#             )
#             self.logger.debug(db_post)
#             return item
#         else:
#             self.overview.update_one(
#                 {'title': item['title']},
#                 {'$set': {
#                     "info.pretty_update_date": item['pretty_update_date'],
#                     'info.now': datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
#                 }}, upsert=True
#             )
#             raise DropItem()
#
#     def print_overview(self):
#         self.open_spider(None)
#         for item in self.overview.find({}):
#             print(item)
#         self.close_spider(None)


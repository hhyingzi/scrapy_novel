# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
from logging import getLogger
from scrapy.exceptions import DropItem
import datetime
import pytz

import configparser

class NovelPipeline:
    def process_item(self, item, spider):
        return item


class MongoPipeline:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('mypass.ini')

        self.mongo_host = '121.40.148.18'
        self.mongo_port = 27017
        self.username = config.get('mongodb', 'mongo_username')
        self.password = config.get('mongodb', 'mongo_password')
        self.authSource = 'admin'  # 用于登录的数据库
        self.db_novel = 'novel'  # 用于写入的数据库
        self.client = pymongo.MongoClient(host=self.mongo_host, port=self.mongo_port, username=self.username,
                                          password=self.password, authSource=self.authSource)

        self.db = self.client[self.db_novel]  # database: novel
        self.overview = self.db['overview']  # collection: overview
        self.detail = self.db['detail']  # collection: detail

        self.logger = getLogger('MyCustomLogger')

    def open_spider(self, spider):
        try:
            self.client.admin.command('ping')
        except pymongo.errors.ConnectionFailure:
            print("Mongodb server not available! ")
            exit(1)
        except pymongo.errors.OperationFailure:
            print('Authentication faild: user:user1, db:db_test')
            exit(1)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        queried = self.overview.find_one({'title': item['title']},
                                         {
                                             'info.last_read_chapter': 1,
                                             'info.update_date': 1
                                         })
        if queried is not None:
            if 'last_read_chapter' not in queried['info']:
                queried_last_read_chapter = None
                queried_update = queried['info']['update_date']
            else:
                queried_last_read_chapter = queried['info']['last_read_chapter']
                queried_update = queried['info']['update_date']
        else:
            queried_last_read_chapter = None
            queried_update = None

        # db_post_test = ItemAdapter(item).asdict()
        db_post = {
            'title': item['title'],
            'info': {
                "author": item['author'],
                "last_read_chapter": queried_last_read_chapter,
                "last_chapter": item['last_chapter'],
                "update_date": item['update_date'],
                "pretty_update_date": item['pretty_update_date'],
                "now": datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
            }
        }

        # 数据库无该书条目则插入，有该书但不是最新则修改 info{'last_chapter', 'update_date', 'pretty_update_date'}, ，否则不做操作
        if queried is None:
            self.overview.insert(db_post)
            self.logger.debug(db_post)
            return item
        elif queried_update != item['update_date']:
            self.overview.update_one(
                {'title': item['title']},
                {'$set': {
                    'info': {
                        "author": item['author'],
                        "last_chapter": item['last_chapter'],
                        "update_date": item['update_date'],
                        "pretty_update_date": item['pretty_update_date'],
                        "now": datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
                    }
                }}, upsert=True
            )
            self.logger.debug(db_post)
            return item
        else:
            self.overview.update_one(
                {'title': item['title']},
                {'$set': {
                    "info.pretty_update_date": item['pretty_update_date'],
                    'info.now': datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
                }}, upsert=True
            )
            raise DropItem()

    def print_overview(self):
        self.open_spider(None)
        for item in self.overview.find({}):
            print(item)
        self.close_spider(None)





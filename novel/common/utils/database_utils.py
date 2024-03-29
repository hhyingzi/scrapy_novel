import configparser
import pymongo


class NovelUtils:
    db_example = [
        'novel'  # 用于写入业务数据的数据库
    ]
    collection_example = [
        'novel_info',  # 用于存放小说基本信息
        'content'  # 用于存储小说具体章节
    ]

    def __init__(self):
        # 加载配置文件
        config = configparser.ConfigParser()
        config.read('../../mypass.ini')

        # 加载数据库配置
        self.mongo_host = config.get('mongodb', 'mongo_host')
        self.mongo_port = int(config.get('mongodb', 'mongo_port'))
        self.mongo_username = config.get('mongodb', 'mongo_username')
        self.mongo_password = config.get('mongodb', 'mongo_password')
        self.authSource = 'admin'  # 用于登录的数据库，需要指定为用户凭据所在位置
        # 建立数据库连接
        self.client = pymongo.MongoClient(host=self.mongo_host,
                                          port=self.mongo_port,
                                          username=self.mongo_username,
                                          password=self.mongo_password,
                                          authSource=self.authSource)
        # 验证数据库连接
        try:
            self.client.admin.command('ping')
            print("MongoDB connect successful.")
        except pymongo.errors.ConnectionFailure:
            print("Mongodb server not available! 服务器无法连接！")
            exit(1)
        except pymongo.errors.OperationFailure:
            print(f'Mongodb Authentication faild! 认证失败！ user:{self.mongo_username}, db:{self.authSource}')
            exit(1)

        # 指定 database: novel
        self.db = self.client['novel']
        # 指定 collection
        self.novel_info_collection = self.db['novel_info']  # novel_info 用于预览小说
        self.content_collection = self.db['content']  # content 用于存储小说具体章节

    def del_novel_info(self, novel_name):
        """删除小说数据 """
        # 删除小说数据
        delete_result = self.novel_info_collection.delete_one({'title': novel_name})
        print(f"Drop novel info :{novel_name} successful!")
        print(f"Deleted {delete_result.deleted_count} documents.")

    def del_novel_and_chapters(self, chapter_name):
        """删除info中的目录信息和content中的章节信息"""

        # 根据小说名称删除 content 表中数据
        delete_result = self.content_collection.delete_many(filter={'book_name': chapter_name})
        print(f"Deleted {delete_result.deleted_count} documents.")
        # 根据小说名删除 info 表中数据
        delete_result = self.novel_info_collection.delete_one({'book_name': chapter_name})
        print(f"Deleted {delete_result.deleted_count} documents.")

    def clear_contents(self):
        pass

    def update_contents(self):
        pass

class ContentUtile:
    def __init__(self):
        pass

    def modify_contents(self):
        pass


class MongodbOperator:
    db_example = [
        'novel'  # 用于写入业务数据的数据库
    ]
    collection_example = [
        'novel_info',  # 用于存放小说基本信息
        'content'  # 用于存储小说具体章节
    ]

    def __init__(self):
        # 加载配置文件
        config = configparser.ConfigParser()
        config.read('../../mypass.ini')

        # 加载数据库配置
        self.mongo_host = config.get('mongodb', 'mongo_host')
        self.mongo_port = int(config.get('mongodb', 'mongo_port'))
        self.mongo_username = config.get('mongodb', 'mongo_username')
        self.mongo_password = config.get('mongodb', 'mongo_password')
        self.authSource = 'admin'  # 用于登录的数据库，需要指定为用户凭据所在位置
        # 建立数据库连接
        self.client = pymongo.MongoClient(host=self.mongo_host,
                                          port=self.mongo_port,
                                          username=self.mongo_username,
                                          password=self.mongo_password,
                                          authSource=self.authSource)
        # 验证数据库连接
        try:
            self.client.admin.command('ping')
            print("MongoDB connect successful.")
        except pymongo.errors.ConnectionFailure:
            print("Mongodb server not available! 服务器无法连接！")
            exit(1)
        except pymongo.errors.OperationFailure:
            print(f'Mongodb Authentication faild! 认证失败！ user:{self.mongo_username}, db:{self.authSource}')
            exit(1)

    def show_db_list(self):
        dblist = self.client.list_database_names()
        print(dblist)

    def drop_db(self, db_name):
        db = self.client[db_name]
        pass

    def show_collection_list(self, db_name):
        """显示所有 collections 的名称"""
        db = self.client[db_name]
        print(db.list_collection_names())

    def drop_collection(self, db_name, collection_name):
        """删除 collection """
        db = self.client[db_name]
        db.drop_collection(collection_name)
        print("Drop collection successful!")

    def clear_collection(self, db_name, collection_name):
        """清空 collection 所有数据"""
        db = self.client[db_name]
        delete_result = db[collection_name].delete_many(filter={})
        print(f"Deleted {delete_result.deleted_count} documents.")

    def get_all_documents(self, db_name, collection_name):
        db = self.client[db_name]
        for document in db[collection_name].find({}, {'_id': 0, 'chapter_name': 1, 'content': 1})[10:20]:
            print(document)

    def get_one_data_example(self, db_name, collection_name):
        db = self.client[db_name]
        collection = db[collection_name]
        data = collection.find_one({})
        return data

if __name__ == "__main__":
    # 获取一条数据示例，以获取数据库结构
    # mongodb_operator = MongodbOperator()
    # example1 = mongodb_operator.get_one_data_example('novel', 'novel_info')
    # example2 = mongodb_operator.get_one_data_example('novel', 'content')
    # print("info: ", example1, "\ncontent: ", example2)

    novelutils = NovelUtils()
    novelutils.del_novel_and_chapters("我的超能力每周刷新")

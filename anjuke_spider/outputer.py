# --*-- coding: utf-8 --*--
import codecs
import csv
import pymongo


class MongoDBIO(object):
    def __init__(self, host, port, name, password, database, collection):
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.database = database
        self.collection = collection

    def Connection(self):
        connection = pymongo.MongoClient(host=self.host, port=self.port)
        # db = connection.datas
        db = connection[self.database]
        if self.name or self.password:
            db.authenticate(name=self.name, password=self.password)
        # print "Database:", db.name
        posts = db[self.collection]
        # print "Collection:", posts.name
        return posts


class MongodbOutputer(object):
    def __init__(self):
        self.save_host = "localhost"
        self.save_port = 27017
        self.save_name = ""
        self.save_password = ""
        self.save_database = "house_info"
        self.save_collection = "zhengzhou"

    def ResultSave(self, save_content):
        posts = MongoDBIO(self.save_host, self.save_port, self.save_name, self.save_password, self.save_database,
                        self.save_collection).Connection()

        posts.save(save_content)

    def ContentSave(self, data_list):
        # 保存配置
        for data in data_list:
            save_content = {
                "name": data['name'],
                "status": data['status'],
                "price": data['price'],
                "discount": data['discount'],
                "location": data['location'],
                "telephone": data['telephone']
            }
            self.ResultSave(save_content)





class CsvOutputer(object):
    def __init__(self):
        self.close_signal = False

    def prepare_csv(self):
        csvfile = open('anjuke_zz.csv', 'wb')
        csvfile.write(codecs.BOM_UTF8)

        writer = csv.writer(csvfile)
        writer.writerow(['名称', '状态', '价格', '折扣', '位置', '特点', '电话'])
        csvfile.close()

    def output_csv(self, data_list):

        csvfile = open('anjuke_zz.csv', 'a+')
        csvfile.write(codecs.BOM_UTF8)

        writer = csv.writer(csvfile)

        try:
            if data_list:
                for data in data_list:
                    value = [data['name'], data['status'], data['price'], data['discount'], data['location'], data['feature'], data['telephone']]
                    # print "******", value
                    writer.writerow(value)
            else:
                pass

        except Exception as e:
            print e

        if self.close_signal:
            csvfile.close()

    def close_csv(self):
        self.close_signal = True

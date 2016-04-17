# --*-- coding: utf-8 --*--
import codecs
import csv
import pymongo


class MongoDBIO:
    # 申明相关的属性
    def __init__(self, host, port, name, password, database, collection):
        self.host = host
        self.port = port
        self.name = name
        self.password = password
        self.database = database
        self.collection = collection

    # 连接数据库，db和posts为数据库和集合的游标
    def Connection(self):
        # connection = pymongo.MongoClient() # 连接本地数据库
        connection = pymongo.MongoClient(host=self.host, port=self.port)
        # db = connection.datas
        db = connection[self.database]
        if self.name or self.password:
            db.authenticate(name=self.name, password=self.password) # 验证用户名密码
        # print "Database:", db.name
        posts = db[self.collection]
        # print "Collection:", posts.name
        return posts



class CsvOutputer(object):
    def __init__(self):
        self.datas = []
        self.close_signal = False

    def collect_data(self, data):
        if len(data) != 0:
            self.datas.append(data)

    def prepare_csv(self):
        csvfile = open('anjuke_zz.csv', 'wb')
        csvfile.write(codecs.BOM_UTF8)

        writer = csv.writer(csvfile)
        writer.writerow(['名称', '状态', '价格', '折扣', '位置'])
        csvfile.close()

    def output_csv(self, data_list):

        csvfile = open('anjuke_zz.csv', 'a+')
        csvfile.write(codecs.BOM_UTF8)

        writer = csv.writer(csvfile)
        for data in data_list:
            value = [data['name'], data['status'], data['price'], data['discount'], data['location']]
            # print "******", value
            writer.writerow(value)

        if self.close_signal:
            csvfile.close()

    def close_csv(self):
        self.close_signal = True



class TxtOutputer(object):
    pass
    # fout = open('output.txt', 'w')
    # for data in self.datas:
    #     if data['title'] and data['year'] and data['director'] and data['rating_num']:
    #     fout.write(data['title'])
    #     fout.write(data['year'])
    #     fout.write(data['director'])
    #     fout.write(data['rating_num'])
    #     fout.write("\n")

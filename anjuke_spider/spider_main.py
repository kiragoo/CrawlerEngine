# --*--coding: utf-8 --*--
import re
import time

import downloader
import content_parser
import outputer

import url_manager


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = downloader.HtmlDownloader()
        self.parser = content_parser.HtmlParser()
        self.outputer = outputer.CsvOutputer()
        self.mongodb_outputer = outputer.MongodbOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)

        self.outputer.prepare_csv()    # 准备csv文件
        while self.urls.has_new_url():
            new_url = self.urls.get_new_url()
            print "[craw %d]: %s" % (count, new_url)

            html_cont = self.downloader.download(new_url)
            new_url, new_data = self.parser.parse(new_url, html_cont)

            print "[new_data]: ", new_data
            self.outputer.output_csv(new_data)    # 写入csv文件

            # self.mongodb_outputer.ContentSave(new_data)

            self.urls.add_new_urls(new_url)

            # if count == 20:
            #     break
            count += 1
        self.outputer.close_csv()    # 关闭csv文件


if __name__ == "__main__":
    root_url = "http://zz.fang.anjuke.com/"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
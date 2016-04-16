# --*--coding: utf-8 --*--
import re
import time

import downloader, parser, outputer

from SPIDER.douban_spider import url_manager


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = downloader.HtmlDownloader()
        self.parser = parser.HtmlParser()
        # self.outputer = outputer.HtmlOutputer()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)

        with open('output.txt', 'a+') as f:
            while self.urls.has_new_url():
                new_url = self.urls.get_new_url()
                print "[craw %d]: %s" % (count, new_url)

                html_cont = self.downloader.download(new_url)
                new_url, new_data = self.parser.parse(new_url, html_cont)

                print "[new_data]: ", new_data

                self.urls.add_new_urls(new_url)

                if count == 20:
                    break
                count += 1

            # self.outputer.output_html()


if __name__ == "__main__":
    root_url = "http://zz.fang.anjuke.com/"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
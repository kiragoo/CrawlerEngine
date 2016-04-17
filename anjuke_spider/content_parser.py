# --*-- coding: utf-8 --*--
import re
import urlparse
from bs4 import BeautifulSoup

import downloader


class HtmlParser(object):

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"http://zz.fang.anjuke.com/loupan/s\?"))
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        data_list = []
        # soup = soup.prettify().encode('utf-8')
        # with open('html_cont.txt', 'wb') as f:
        #     f.writelines(soup)
        if soup:
            items = soup.find_all('div', attrs={"data-soj": re.compile("AF_RANK")})
            # print len(items)
            for item in items:
                res_data = {}
                try:
                    name = item.find('a', class_='items-name').string   # 房产名称
                    status = item.find_all('i', class_='status-icon')[0].string  # 状态(待售,在售)
                    price = item.find('p', class_='price').find('span').string  # 参考价格
                    discount = item.find('em', class_='discount-txt').string    # 折扣优惠
                    location = item.find('p', class_='address').find('a', class_='list-map').string.rstrip('...')  # 地理位置
                    link = item.find('a', class_='items-name')['href']
                    code = link.split('/')[-1].split('.')[0]
                    # comment = self.get_comment(code) # 网友评论
                    #
                    # print name, len(comment)
                    # print '---------'


                except:
                    continue

                try:
                    res_data['name'] = name
                    res_data['status'] = status
                    res_data['price'] = price
                    res_data['discount'] = discount
                    res_data['location'] = location
                    # res_data['comment'] = comment
                    data_list.append(res_data)
                except:
                    pass

            return data_list

    def get_comment(self, code):
        comment = []
        DL = downloader.HtmlDownloader()
        # print '----', code
        url = "http://zz.fang.anjuke.com/loupan/dianping-%s.html?from=commview_dp_moretop" % code
        # print 'comment url', url
        html_cont = DL.download(url)
        comment += self.pase_comment(html_cont)

        page_num = 2
        global end_page
        end_page = False
        while True:
            url = "http://zz.fang.anjuke.com/loupan/dianping-%s.htmls/?from=commview_dp_moretop&p=%s" % (code, page_num)
            # print 'comment url', url
            html_cont = DL.download(url)
            page_num += 1
            comment += self.pase_comment(html_cont)
            if end_page:
                break
        return comment

    def pase_comment(self, html_cont):
        comment_list = []
        C = {}
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        if soup:

            if soup.find('span', class_='stat-disable'):
                global end_page
                end_page = True

            items = soup.find('ul', class_='total-revlist').find_all('li')

            for item in items:
                try:
                    user = item.find('span', class_='author').string
                    content = item.find('h4').string.strip()
                    date = item.find('span', class_='date').string
                except:
                    continue

                C['user'] = user
                C['content'] = content
                C['date'] = date
                comment_list.append(C)
        return comment_list

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')

        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)

        return new_urls, new_data


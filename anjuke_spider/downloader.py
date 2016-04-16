import urllib2


class HtmlDownloader(object):
    def __init__(self):
        pass

    def download(self, url):
        if url is None:
            return None

        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        data = None
        request = urllib2.Request(url, data, headers)

        response = urllib2.urlopen(request)
        if response.getcode() != 200:
            return None

        return response.read()
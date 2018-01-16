import urllib.request
import urllib.parse
from urllib import request
import json, time
from bs4 import BeautifulSoup

from html.parser import HTMLParser
from html.entities import name2codepoint


def get_attr(attrs, attrname):
    for attr in attrs:
        if attr[0] == attrname:
            return attr[1]
    return None


class MyHTMLParser(HTMLParser):
    def __init__(self, convert_charrefs=True):
        super().__init__(convert_charrefs=True)
        self.shouldRead = False
        self.shouldReadPhone = False

    def handle_starttag(self, tag, attrs):
        if tag == 'span':
            class_name = get_attr(attrs, 'class')
            if class_name == 'a color':
                self.shouldRead = True
            if class_name == 'color':
                self.shouldReadPhone = True
        if tag == 'a':
            href = get_attr(attrs, 'href')
            if href is None:
                return
            if "uin=" in href:
                self.shouldRead = True
                print('href:', href)
        if tag == 'p':
            class_name = get_attr(attrs, 'class')
            if class_name == 'lhag':
                self.shouldRead = True

    def handle_endtag(self, tag):
        if self.shouldRead:
            self.shouldRead = False

    def handle_startendtag(self, tag, attrs):
        return

    def handle_data(self, data):
        if self.shouldRead:
            print("data:", data)
        if self.shouldReadPhone:
            print("data:", data)
            self.shouldReadPhone = False

    def handle_comment(self, data):
        return

    def handle_entityref(self, name):
        print('handle_entityref:%s' % name)

    def handle_charref(self, name):
        print('handle_charref:%s' % name)

    def handle_pi(self, data):
        print('handle_pi:%s' % data)


def collectBeauty():
    # url = 'http://nanrenvip.net/find.html'
    # req = urllib.request.Request(url)
    # req.add_header('Host', 'nanrenvip.net')
    # req.add_header('Connection', 'keep-alive')
    # req.add_header('Cache-Control', 'max-age=0')
    # req.add_header('User-Agent',
    #                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36')
    # req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    # req.add_header('Cookie',
    #                'Hm_lvt_3c484b51b01288268c9a10f4c7f31cdf=1500941316; Hm_lpvt_3c484b51b01288268c9a10f4c7f31cdf=1500941321')
    # req.add_header('Accept-Encoding', 'gzip, deflate')
    # req.add_header('Referer', 'http://nanrenvip.net/old.html')
    # req.add_header('If-Modified-Since', 'Thu, 20 Jul 2015 06:42:38 GMT')
    # req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
    # req.add_header('Upgrade-Insecure-Requests', '1')
    # params = json.dumps({'keyword': '产业投资'})
    # params = bytes(params, 'utf8')
    # response = urllib.request.urlopen(req)
    # code = response.status
    # print("%d" % code)
    # print(response.info())
    # result = response.read().decode('utf-8')
    # print(result)
    with request.urlopen('http://www.bx58.com/agentPepole.html') as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        resultHtml = data.decode('utf-8')
        # print('Data:', resultHtml)
        parser = MyHTMLParser()
        parser.feed(resultHtml)
    return


collectBeauty()

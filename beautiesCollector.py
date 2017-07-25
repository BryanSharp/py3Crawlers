import urllib.request
import urllib.parse
from urllib import request
import json, time
from bs4 import BeautifulSoup


from html.parser import HTMLParser
from html.entities import name2codepoint

class MyHTMLParser(HTMLParser):

    def handle_starttag(self, tag, attrs):
        print('<%s>' % tag)

    def handle_endtag(self, tag):
        print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        print('<%s/>' % tag)

    def handle_data(self, data):
        print(data)

    def handle_comment(self, data):
        print('<!--', data, '-->')

    def handle_entityref(self, name):
        print('&%s;' % name)

    def handle_charref(self, name):
        print('&#%s;' % name)


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
    with request.urlopen('http://nanrenvip.net/find.html') as f:
        data = f.read()
        print('Status:', f.status, f.reason)
        for k, v in f.getheaders():
            print('%s: %s' % (k, v))
        resultHtml = data.decode('utf-8')
        print('Data:', resultHtml)
        parser = MyHTMLParser()
        parser.feed(resultHtml)
    return


collectBeauty()

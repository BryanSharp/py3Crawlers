import urllib.request
import time


def getStockCode(counter, prefix="0"):
    if counter < 10:
        stockCode = '%s0000%d' % (prefix, counter)
    elif counter < 100:
        stockCode = '%s000%d' % (prefix, counter)
    elif counter < 1000:
        stockCode = '%s00%d' % (prefix, counter)
    elif counter < 10000:
        stockCode = '%s0%d' % (prefix, counter)
    elif counter < 100000:
        stockCode = '%s%d' % (prefix, counter)
    else:
        stockCode = '%d' % counter
    return stockCode


def collectStockCode(marketname, prefix="6",isSM=False):
    counter = 0
    index = 0
    stockMap = {}
    stockCode = ""
    while counter < 4000:
        if counter == 2000:
            counter += 1000
        stockCode = getStockCode(counter, prefix)
        url = 'http://hq.sinajs.cn/list=%s%s' % (marketname, stockCode)
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla')
        response = urllib.request.urlopen(req)
        print(response.info())
        html = response.read().decode('GBK')
        if len(html) > 30:
            start = html.find("\"")
            end = html.find(",")
            stockName = html[start + 1:end]
            stockMap[stockCode] = stockName
            index += 1
            print("new stock found %s" % stockName)
        print(html)
        counter += 1
        time.sleep(0.05)
    if isSM:
        #创业板
        txt_name = '%s%s.txt' % (marketname, 'SM-code-info')
    else:
        txt_name = '%s%s.txt' % (marketname, '-code-info')
    with open(txt_name, 'wb') as f:
        content = stockMap.__str__() + "\n%s总数量是%d" % (marketname, len(stockMap))
        f.write(content.encode())
    return txt_name


# print(stockMap)
# response = urllib.request.urlopen('http://image.sinajs.cn/newchart/daily/n/sh601006.gif')
# with open('newImage.gif', 'wb') as f:
#     f.write(response.read())
# response = urllib.request.urlopen('http://image.sinajs.cn/newchart/daily/n/sh601006.gif')
def restructure(filename):
    print('going to restructure')
    content = ""
    with open(filename, 'rb') as f:
        content = f.read().decode("utf-8")
    content = content.replace("\'", "\"")
    huIndex = content.find("总数", len(content) - 20) - 2
    newForm = content[0:huIndex - 1]
    newForm = newForm.replace(",", "\n,")
    with open('%s-restructure.txt' % filename[0:-4], 'wb') as f:
        f.write(newForm.encode())

def getAllCodes():
    filename = collectStockCode("sh")
    restructure(filename)
    filename = collectStockCode("sz", '0')
    restructure(filename)
    filename = collectStockCode("sz", '3', True)
    restructure(filename)



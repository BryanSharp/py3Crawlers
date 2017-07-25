import urllib.request
import urllib.parse
import json, time
from bs4 import BeautifulSoup
import csv


# doc:https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
def timeMilli2Date(timeMillis):
    return time.strftime("%Y-%m-%d", time.localtime(timeMillis / 1000))


def collectStockCode(keyword, pages=200):
    url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.22292638394801246&page=0&size=%d' % pages
    req = urllib.request.Request(url)
    fakeHeaders(req)
    params = json.dumps({'keyword': keyword})
    params = bytes(params, 'utf8')
    response = urllib.request.urlopen(req, params)
    result = response.read().decode('utf8')
    full_json = json.loads(result)
    content_arr = full_json["content"]
    printTitle = False
    print('总长度%d' % len(content_arr))
    cvsArrs = []
    counter = 0
    corpName = ''
    for corp in content_arr:
        corpUrl = 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/%s' % corp["url"]
        try:
            req = urllib.request.Request(corpUrl)
            fakeHeaders(req)
            response = urllib.request.urlopen(req)
        except:
            print('网络连接出现问题，网址：%s' % corpUrl)
            continue
        soup = BeautifulSoup(response.read().decode())
        titles = soup.find_all(attrs={'class': 'td-title'})
        contents = soup.find_all(attrs={'class': 'td-content'})
        firstRow = []
        if not printTitle:
            printTitle = True
            for t in titles:
                if '机构诚信' in t.text:
                    continue
                titleStr = t.text.strip().replace(':', '')
                firstRow.append(titleStr)
            cvsArrs.append(firstRow)
        i = 0
        row = []
        for ct in contents:
            if i == 0:
                i += 1
                continue
            ct = ct.text.strip().replace('\n', '').replace(' ', '').replace('\t', '')
            if i == 1:
                ct = ct.split('\xa0')[0]
                corpName = ct
            row.append(ct)
            i += 1
            if i > 19:
                break
        counter += 1
        print('解析完成第%d条,对应公司：%s' % (counter, corpName))
        cvsArrs.append(row)
    write2Csv(cvsArrs, keyword)
    return


def write2Csv(cvsArrs, keyword):
    # 这里一定要加上encoding属性 不然会造成乱码
    # csv 文档 ： https://docs.python.org/3/library/csv.html
    with open('%s.csv' % keyword, "w", newline="", encoding='utf-8') as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvWriter = csv.writer(datacsv, dialect="excel")
        for arr in cvsArrs:
            csvWriter.writerow(arr)


def fakeHeaders(req):
    req.add_header('Host', 'gs.amac.org.cn')
    req.add_header('Origin', 'http://gs.amac.org.cn')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Connection', 'keep-alive')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Referer', 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36')
    # req.add_header('Accept-Encoding', 'gzip, deflate')
    # 上面这句如果加上会导致服务器返回gzip内容
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')


'''
{
    "id": "101000000739",
    "managerName": "广州越秀<em>产业投资</em>基金管理股份有限公司",
    "artificialPersonName": "王恕慧",
    "registerNo": "P1000696",
    "establishDate": 1312156800000,
    "managerHasProduct": null,
    "url": "101000000739.html",
    "registerDate": 1396310400000,
    "registerAddress": "广东省广州市天河区珠江西路5号广州国际金融中心63层",
    "registerProvince": "广东省",
    "registerCity": "广州市",
    "regAdrAgg": "广东省",
    "fundCount": 17,
    "fundScale": 1755326.2139,
    "paidInCapital": 1220161.2039,
    "subscribedCapital": 2163347.2139,
    "hasSpecialTips": false,
    "inBlacklist": false,
    "hasCreditTips": false,
    "regCoordinate": "23.123886896807683,113.32937730581973",
    "officeCoordinate": "23.123886896807683,113.32937730581973",
    "officeAddress": "广东省广州市天河区珠江西路5号广州国际金融中心主塔写字楼第63层01-A、E单元",
    "officeProvince": "广东省",
    "officeCity": "广州市",
    "primaryInvestType": null
}
'''

'''POST  HTTP/1.1
POST /amac-infodisc/api/pof/manager?rand=0.22282638394801246&page=0&size=20 HTTP/1.1
Host: gs.amac.org.cn
Connection: keep-alive
Content-Length: 26
Accept: application/json, text/javascript, */*; q=0.01
Origin: http://gs.amac.org.cn
X-Requested-With: XMLHttpRequest
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36
Content-Type: application/json
Referer: http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.8,en;q=0.6
'''

collectStockCode('股权投资', 2350)
# collectStockCode('产业投资')
# with open("infos.csv", "w", newline="",encoding='utf-8') as datacsv:
#     # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
#     csvwriter = csv.writer(datacsv, dialect=("excel"))
#     # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
#     csvwriter.writerow(['你好', '再见'])

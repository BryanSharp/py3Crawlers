import urllib.request
import urllib.parse
import json, time
from bs4 import BeautifulSoup
# doc:https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh/
def timeMilli2Date(timeMillis):
    return time.strftime("%Y-%m-%d", time.localtime(timeMillis / 1000))


def collectStockCode():
    counter = 0
    index = 0
    stockMap = {}
    stockCode = ""
    url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/manager?rand=0.22292638394801246&page=0&size=130'
    req = urllib.request.Request(url)
    req.add_header('Host', 'gs.amac.org.cn')
    req.add_header('Origin', 'http://gs.amac.org.cn')
    req.add_header('Accept', 'application/json, text/javascript, */*; q=0.01')
    req.add_header('Connection', 'keep-alive')
    req.add_header('X-Requested-With', 'XMLHttpRequest')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Referer', 'http://gs.amac.org.cn/amac-infodisc/res/pof/manager/index.html')
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
    params = json.dumps({'keyword': '产业投资'})
    params = bytes(params, 'utf8')
    response = urllib.request.urlopen(req, params)
    print(response.info())
    result = response.read().decode('utf8')
    print(result)
    json_load = json.loads(result)
    content_arr = json_load["content"]
    for corp in content_arr:
        info = "%s\t%s\t%s\t%s\t%s" % (
            corp["managerName"].replace('<em>','').replace('</em>',''),
            timeMilli2Date(corp["establishDate"]),
            timeMilli2Date(corp["registerDate"]),
            corp["artificialPersonName"],
            corp["officeAddress"]
        )
        corpUrl='http://gs.amac.org.cn/amac-infodisc/res/pof/manager/%s' % corp["url"]
        req = urllib.request.Request(corpUrl)
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
        req.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
        response = urllib.request.urlopen(req)
        soup = BeautifulSoup(response.read().decode())
        print(soup.find_all(attrs={'class':'td-content'}))
        print(info)
    print(content_arr)
    with open('temp.txt', 'wb') as f:
        f.write(result.encode())
    return

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

collectStockCode()

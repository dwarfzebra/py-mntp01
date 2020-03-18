import grequests
import json
import requests
urls = ["http://www.baidu.com", "http://www.baidu.com", "http://www.baidu.com"]
req = (grequests.get(u) for u in urls)
resp = grequests.map(req)

for res in resp:
    res.encoding='utf-8'
    print(res.text)

list=[]
list.append('a')
list.append('b')
print(list)

keyword = str('杨晨晨'.encode('gb2312'))
button = str('搜索'.encode('gb2312'))
data = {
    'keyword': keyword,
    'button': button
}
url = "https://www.mntp01.com/plus/search/index.asp"
r = requests.post(url, data=data)

import grequests
import os
import re
import requests


# 异常处理
def exception_handler(request, exception):
    print("Request failed")


# 创建目录
def create_target_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


# 根据图片路径下载图片
def download_img(img_url_list, dir):
    base_url = 'https://www.mntp01.com/'
    # 请求头
    req = (grequests.get(base_url + u, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'referer': base_url + u
    }) for u in img_url_list)
    print('发起请求')
    res_list = grequests.map(req, size=15, exception_handler=exception_handler)
    print('得到结果')
    for res in res_list:
        try:
            # 图片名称正则
            img_name_p = '/\d+/\d+(/.*?jpg)'
            # 要保存的图片名
            img_name = re.search(img_name_p, res.url).group(1)
            with open(dir + '/' + img_name, 'wb') as f:
                f.write(res.content)
                print('下载一张')
        except:
            print('下载失败' + res)


# 根据页面路径下载
def download_by_url(url_list):
    base_url = 'https://www.mntp01.com'
    res_list = grequests.map((grequests.get(base_url + url) for url in url_list), size=15,
                             exception_handler=exception_handler)
    down_list = []
    for index, res in enumerate(res_list):
        # 设置编码格式
        res.encoding = 'gb2312'
        dir_name_p = '//.*?/(.*?/)'
        dir_result = re.search(dir_name_p, res.url)
        # 内容
        text = res.text
        # 人物名称 正则
        person_p = '写真美女.*?>(.*?)<'
        # 人物名称
        person = re.search(person_p, text).group(1)
        # 主题正则
        title_p = 'keywords.*?content="(.*?)"/>'
        # 主题
        title = re.search(title_p, text).group(1)
        dir_name = dir_result.group(1) + person + '/' + title
        create_target_dir(dir_name)
        # 目标图片连接正则
        img_p = 'onload.*?src="(.*?.jpg)"'
        # 图片连接集合
        list = re.findall(img_p, res.text)

        down_list += list
        if ((index + 1) % 5 == 0 or index == len(res_list) - 1):
            download_img(down_list, dir_name)
            down_list = []


# 根据主题下载
def download_by_title(url_list):
    print(url_list)
    base_url = 'https://www.mntp01.com'
    resp = grequests.map((grequests.get(base_url + url) for url in url_list), exception_handler=exception_handler)
    print(resp)
    for res in resp:
        # 设置编码格式
        res.encoding = 'gb2312'
        # 页码正则
        pattern = 'href="(.*?html).*?>\d+<'
        # 页码
        results = re.findall(pattern, res.text)
        download_by_url(results)


mode = print("请选择模式:1. 根据url\n2. 根据搜索关键字")
if mode == '1':
    url = print("输入url:\n")
    list = [].append(url)
    download_by_title(list)
elif mode == '2':
    keyword = input("请输入关键词：\n")
    base_url = 'https://www.mntp01.com'
    search_url = base_url + '/plus/search/index.asp'
    keyword = keyword.encode('gb2312')
    button = '搜索'.encode('gb2312')
    data = {
        'keyword': keyword,
        'button': button
    }
    r = requests.post(search_url, data=data)
    # 搜索结果页面正则
    search_p = '<a href="(\?keyword=.*?)"'
    search_list = re.findall(search_p, r.text)
    print(search_list)
    page_list = grequests.map(grequests.get(search_url + page_url) for page_url in search_list)
    # 每页搜索结果
    for page in page_list:
        print(page)
        result_p = 'title1.*?href="(.*?)"'
        result_list = re.findall(result_p, page.text)
        print(result_list)
        download_by_title(result_list)
else:
    print("退出程序")

import requests
import re
import os

# 创建目录
def create_target_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def download_img(url, dir_name):
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' +
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
        'referer': url
    }
    try:
        # 图片响应
        img = requests.get(url, headers=headers)

        # 图片名称正则
        img_name_p = '/\d+/\d+(/.*?jpg)'
        # 要保存的图片名
        img_name = re.search(img_name_p, url).group(1)

        # 保存图片
        with  open(dir_name + '/' + img_name, 'wb') as f:
            f.write(img.content)
            print('下载成功一张')
    except:
        print("下载失败" + url)


# 根据url下载主题图片
def download_by_url(url):
    # 访问地址
    # 基础url正则
    domain_p = '(https://.*?/)'
    base_url = re.search(domain_p, url).group(1)
    res = requests.get(url)
    # 设置编码格式
    res.encoding = 'gb2312'

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

    # 页码正则
    pattern = 'href="(.*?html).*?>\d+<'

    # 页码
    results = re.findall(pattern, text)
    for result in results:
        # 详情页url
        sub_url = base_url + result
        # 打开详情页  获取图像地址
        sub_res = requests.get(sub_url)
        # 详情页编码格式
        sub_res.encoding = 'utf-8'

        # 目标图片连接正则
        img_p = 'onload.*?src="(.*?.jpg)"'
        # 图片连接集合
        img_url_list = re.findall(img_p, sub_res.text)

        for imgUrl in img_url_list:
            # 图片下载地址
            download_url = base_url + imgUrl

            # 要下载目录名称正则
            dir_name_p = '/(.*?/)'
            dir_result = re.search(dir_name_p, result)
            # 目录名
            dir_name = dir_result.group(1) + person + '/' + title
            #  创建目录
            create_target_dir(dir_name)
            download_img(download_url, dir_name)


# 打开搜索结果页
def open_search_result(url):
    res = requests.get(url)
    result_p = 'title1.*?href="(.*?)"'
    result_list = re.findall(result_p, res.text)
    for result in result_list:
        download_url = 'https://www.mntp01.com' + result
        download_by_url('https://www.mntp01.com/' + result)


mode = input("请选择下载模式：\n1. 输入url:  (https//*******)\n2. 输入关键词：\n")
if mode == '1':
    value = input("请输入url：\n")
    download_by_url(value)
elif mode == '2':
    keyword = input("请输入关键词：\n")
    search_url = 'https://www.mntp01.com/plus/search/index.asp'
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

    print(type(search_list))
    # 页面列表
    for search_result in search_list:
        page_url = search_url + search_result
        open_search_result(page_url)
else:
    print("输入错误，退出")

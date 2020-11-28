import re
import requests
from urllib import error
import _thread
from bs4 import BeautifulSoup
import os
import time

file = ''
List = []


def dowmloadPicture(html, keyword, num=0, numpics=40):
    num = num
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 先利用正则表达式找到图片url
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    d_start = time.time()
    for each in pic_url:
        print('正在下载 ' + str(keyword) + ' 第 ' + str(num + 1) + ' 张图片')
        try:
            if each is not None:
                pic = requests.get(each, timeout=7)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = 'Irish_picture/pics_' + str(keyword) + r'\\' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numpics:
            d_end = time.time()
            print(str(keyword) + ' 下载完毕. 耗时: {0}秒'.format(d_end - d_start))
            return


def down_word_thread(word, num_pics):
    print('Start a new thread')
    headers = {
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Upgrade-Insecure-Requests': '1'
    }

    req = requests.Session()
    req.headers = headers

    ###############################

    tm = 40

    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='

    file = 'pics_' + word
    if not os.path.exists('Irish_picture/' + file):
        os.mkdir('Irish_picture/' + file)
        t = 0
        tmp = url
        while t < tm:
            try:
                url = tmp + str(t)
                # result = requests.get(url, timeout=10)
                result = req.get(url, timeout=5, allow_redirects=False)
                print(url)
            except error.HTTPError as e:
                print('网络错误，请调整网络后重试')
                t = t + 60  # 翻页
            else:
                dowmloadPicture(result.text, word, 0, num_pics)
                t = t + 60
    else:
        print('该文件夹已存在.')


if __name__ == '__main__':  # 主函数入口

    start = time.time()
    num_pics = int(input('每个爬多少？：'))
    with open('./name.txt', encoding='utf-8') as file:
        line_list = [k.strip() for k in file.readlines()]  # 用 strip()移除末尾的空格
    n_words = len(line_list)
    i = 0
    try:
        while i < n_words:
            _thread.start_new_thread(down_word_thread, (line_list[i], num_pics))
            i += 1
            time.sleep(1)
        time.sleep(250)
        # 5个250秒 6个280秒 一次别写太多词

    except(error):
        print(error)
        print("Error: 无法启动线程")
    end = time.time()
    print('耗时:', end - start)
    print('当前搜索结束，感谢使用')

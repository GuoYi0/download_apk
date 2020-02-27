# coding=utf-8
from six.moves import urllib
import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Queue, Process
import traceback
import json


def parser_apks(root_path, pages, thread_id):
    log = open("log%d.txt" % thread_id, "w")
    local_path = "F:\\huawei_apk\\game"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    for page in pages:
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        try:
            url = root_path + str(page)
            wbdata = requests.get(url, headers=headers).text.encode("latin1").decode("utf-8")  # url就是待解析页面的浏览器地址
            soup = BeautifulSoup(wbdata, "html.parser")
            if "错误" in soup.head.title.string:  # 这个页面没有
                continue
            items = soup.find("body").find("div", class_="lay-body").find("div",class_="lay-main")
            # print(items)
            items = items.find("div", class_="lay-left corner").find("div", class_="unit nofloat prsnRe").find("div", class_="unit-main")
            items = items.find_all("div", class_="list-game-app dotline-btn nofloat")
        except Exception as e:
            traceback.print_exc(file=log)
            traceback.print_exc()
            continue
        for item in items:
            # try:
            #     print(item)
            app_info = item.find("div", class_="game-info whole").find("div", class_="app-btn").find('a').get("onclick")
            app_info = app_info.strip(';').strip("zhytools.downloadApp").split(',')
            app_name = app_info[1].strip("'")
            download_url = app_info[5].strip("'")
            if os.path.isfile(os.path.join(local_path, app_name + '.apk')):
                continue
            download_url = app_info[1].get("appdownurl")
            urllib.request.urlretrieve(download_url, os.path.join(local_path, app_name + '.apk'))
            print(app_name, " download successfully!", file=log)
            print(app_name, " download successfully!")
            # except Exception as e:
            #     traceback.print_exc(file=log)
            #     print(app_name, "failed!")
            #     continue
    log.close()
    print("thread %d done!" % thread_id)

parser_apks("https://appstore.huawei.com/game/list_2_0_", [1],0)
# # headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.63 Safari/537.36'}
# headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
#
# wbdata = requests.get("https://appstore.huawei.com/", headers=headers).text.encode("latin1").decode("utf-8")  # url就是待解析页面的浏览器地址
# print(wbdata)
# # soup = BeautifulSoup(wbdata, "html.parser")

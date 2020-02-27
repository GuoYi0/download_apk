# coding=utf-8
from six.moves import urllib
import requests
from bs4 import BeautifulSoup
import os
from multiprocessing import Queue, Process
import traceback

"""
打开一个应用商城，按F12查看网页的html，点击左上角的箭头，再点击要下载的apk，就能看到这个apk对应的html源码了
"""
# 有些应用商城不让爬虫，下面这个HEADERS是为了模拟浏览器。
# 只需要知道浏览器的User-Agent就行。具体可以百度如何获取浏览器的User-Agent
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}


page2category = {
    358: "购物比价",
    23: "影音娱乐",
    24: "实用工具",
    27: "便捷生活",
    361: "旅游住宿",
    33: "拍摄美化",
    345: "新闻阅读",
    26: "社交通讯",
    25: "金融理财",
    30: "教育",
    28: "出行导航",
    359: "没食",
    360: "汽车",
    362: "商务",
    363: "儿童",
    31: "运动健康",
    29: "主题个性"
}
page2category_game = {
    20: "角色扮演",
    15: "休闲益智",
    16: "经营策略",
    22: "体育竞速",
    21: "棋牌桌游",
    18: "动作射击"
}

def parser_apks(root_path, pages, path, thread_id):
    log = open("log%d.txt" % thread_id, "w", encoding='utf-8')
    for page in pages:
        print(page, " start")
        local_path = os.path.join(path, page2category_game[page])
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        for sub_page in range(5):
            url = root_path + str(page)+'_0_'+str(sub_page)
            try:
                wbdata = requests.get(url, headers=HEADERS).text.encode("latin1").decode("utf-8")  # url就是待解析页面的浏览器地址
                soup = BeautifulSoup(wbdata, "html.parser")
                items = soup.find("body").find("div", class_="lay-body").find("div", class_="lay-main")
                items = items.find("div", class_="lay-left corner").find("div", class_="unit nofloat prsnRe").find("div",
                                                                                                                   class_="unit-main")
                items = items.find_all("div", class_="list-game-app dotline-btn nofloat")
            except Exception as e:
                traceback.print_exc(file=log)
                traceback.print_exc()
                continue
            for item in items:
                app_name = None
                try:
                    app_info = item.find("div", class_="game-info whole").find("div", class_="app-btn").find('a').get(
                        "onclick")
                    app_info = app_info.strip(';').strip("zhytools.downloadApp").split(',')
                    app_name = app_info[1].strip().strip("'")
                    download_url = app_info[5].strip().strip("'")
                    if os.path.isfile(os.path.join(local_path, app_name + '.apk')):
                        continue
                    dest = os.path.join(local_path, app_name + '.apk')
                    if os.path.isfile(dest) or os.path.exists(dest):
                        continue
                    urllib.request.urlretrieve(download_url, dest)
                    print(app_name, " download successfully!", file=log)
                    print(app_name, " download successfully!")
                    log.flush()
                except Exception as e:
                    traceback.print_exc(file=log)
                    log.flush()
                    if app_name is not None:
                        print(app_name, "failed!")
                    else:
                        print("something wrong")
                    continue
        print(page, " done!")
        print(page, " done!", file=log)
        log.flush()
    log.close()


def main():
    game_path = "https://appstore.huawei.com/game/list_"
    pages = list(page2category_game.keys())
    num_thread = 3
    num_pages = len(pages)
    num_page_per_thread = num_pages / num_thread
    procs = []
    local_path = "F:\\huawei_apk\\游戏\\"
    for i in range(num_thread):
        start = int(i * num_page_per_thread)
        end = min(int((i + 1) * num_page_per_thread), num_pages)
        split = pages[start:end]
        proc = Process(target=parser_apks, args=(game_path, split, local_path, i))
        print('process:%d, start:%d, end:%d' % (i, start, end))
        proc.start()
        procs.append(proc)
    print("=================================================================================================")
    for p in procs:
        p.join()
        print(p, " done!")


if __name__ == "__main__":
    main()
    print("all done!")

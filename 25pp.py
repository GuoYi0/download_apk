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
ROOT_PATH = "https://www.25pp.com/android/soft/fenlei/"


def parser_apks(pages, thread_id):
    log = open("log%d.txt" % thread_id, "w")
    for page in pages:
        local_path = os.path.join("F:\\25pp_apk", str(page))
        if not os.path.exists(local_path):
            os.makedirs(local_path)

        for sub in range(1, 25):
            try:
                print("page %d, subpage %d " % (page, sub), file=log)
                print("page %d, subpage %d " % (page, sub))
                if sub == 1:
                    url = ROOT_PATH + str(page) + '/'
                else:
                    url = ROOT_PATH + str(page) + '/%d/' % sub
                wbdata = requests.get(url).text  # url就是待解析页面的浏览器地址
                soup = BeautifulSoup(wbdata, "html.parser")
                if "错误" in soup.head.title.string:  # 这个页面没有
                    continue
                items = soup.find("body").find("div", class_="wrap clearfix mb30").find("div",
                                                                                        class_="cate-list-right").find(
                    "div", class_="cate-list-main mt10")
                items = items.find("ul", class_="app-list clearfix").find_all("li")
            except Exception as e:
                traceback.print_exc(file=log)
                traceback.print_exc()
                continue
            for item in items:
                try:
                    app_info = item.find("div", class_="app-info").find_all('a')
                    app_name = app_info[0].string
                    if os.path.isfile(os.path.join(local_path, app_name + '.apk')):
                        continue
                    download_url = app_info[1].get("appdownurl")
                    urllib.request.urlretrieve(download_url, os.path.join(local_path, app_name + '.apk'))
                    print(app_name, " download successfully!", file=log)
                    print(app_name, " download successfully!")
                except Exception as e:
                    traceback.print_exc(file=log)
                    print(app_name, "failed!")
                    continue
    log.close()
    print("thread %d done!" % thread_id)


def main():
    pages = [5014, 5015, 5016, 5017, 5018, 5019, 5020, 5021, 5022, 5023, 5024, 5026, 5027, 5028, 5029]
    num_thread = 4
    num_pages = len(pages)
    num_page_per_thread = num_pages / num_thread
    procs = []
    for i in range(num_thread):
        start = int(i * num_page_per_thread)
        end = min(int((i + 1) * num_page_per_thread), num_pages)
        split = pages[start:end]
        proc = Process(target=parser_apks, args=(split, i))
        print('process:%d, start:%d, end:%d' % (i, start, end))
        proc.start()
        procs.append(proc)

    for p in procs:
        p.join()
        print(p, " done!")


if __name__ == "__main__":
    main()
    print("all done!")

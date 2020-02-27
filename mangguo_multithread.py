# coding=utf-8
import urllib
import requests
import re
from bs4 import BeautifulSoup
import os
from IPython import embed
from multiprocessing import Queue, Process
"""
打开一个应用商城，按F12查看网页的html，点击左上角的箭头，再点击要下载的apk，就能看到这个apk对应的html源码了
"""

def parser_apks(count=30):
    for page in range(40, 51, 1):
        for idx in range(1, 10, 1):
            wbdata = requests.get("http://www.90370.com/apk/s_{}_{}.html".format(page, idx)).text
            print("开始爬取第" + str(page) + "页， 第"+str(idx)+"小页")
            soup = BeautifulSoup(wbdata, "html.parser")
            items = soup.find_all("p")
            result={}
            if page == 40 and idx == 1:
                items = items[9:]
            for item in items:
                try:
                    apk_name = str(item.find_all("a")[0].i.string).encode("latin1").decode("gb2312")
                    url = item.find_all("a")[1].get("href")
                except AttributeError:
                    continue
                except IndexError:
                    continue
                except:
                    print("unkonwn Error")
                    continue
                if apk_name not in result:
                    result[apk_name] = url
                    path = os.path.join("E:\\zsm\\apk", apk_name+'.apk')
                    link = urllib.parse.urljoin("http://www.90370.com", url)
                    try:
                        urllib.request.urlretrieve(link, path)
                    except:
                        print(link, "  not found")
                        continue


def worker(pages):
    for page in pages:
        for idx in range(1, 10, 1):
            wbdata = requests.get("http://www.90370.com/apk/s_{}_{}.html".format(page, idx)).text
            print("开始爬取第" + str(page) + "页， 第"+str(idx)+"小页")
            soup = BeautifulSoup(wbdata, "html.parser")
            items = soup.find_all("p")
            result={}
            if page == 40 and idx == 1:
                items = items[9:]
            for item in items:
                try:
                    apk_name = str(item.find_all("a")[0].i.string).encode("latin1").decode("gb2312")
                    url = item.find_all("a")[1].get("href")
                except AttributeError:
                    continue
                except IndexError:
                    continue
                except:
                    print("unkonwn Error")
                    continue
                if apk_name not in result:
                    result[apk_name] = url
                    path = os.path.join("E:\\zsm\\apk", apk_name+'.apk')
                    link = urllib.parse.urljoin("http://www.90370.com", url)
                    try:
                        urllib.request.urlretrieve(link, path)
                    except:
                        print(link, "  not found")
                        continue



def main():
    pages = [11, 13, 24, 25,19, 20, 6, 21, 22, 23, 12, 18, 17, 16, 15, 14, 10,
             9, 8, 7, 5, 4, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]
    num_thread = 4
    num_pages = len(pages)
    num_page_per_thread = num_pages / num_thread
    procs = []
    for i in range(num_thread):
        start = int(i*num_page_per_thread)
        end = min(int((i+1)*num_page_per_thread), num_pages)
        split = pages[start:end]
        proc = Process(target=worker, args=(split, ))
        print('process:%d, start:%d, end:%d' % (i, start, end))
        proc.start()
        procs.append(proc)

    for p in procs:
        p.join()


if __name__ == "__main__":
    main()

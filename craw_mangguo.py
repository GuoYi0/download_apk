# coding=utf-8
import urllib
import requests
import re
from bs4 import BeautifulSoup
import os
from IPython import embed
from multiprocessing import Queue, Process


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
                    path = os.path.join("F:\\apk_sub", apk_name+'.apk')
                    link = urllib.parse.urljoin("http://www.90370.com", url)
                    try:
                        urllib.request.urlretrieve(link, path)
                    except:
                        print(link, "  not found")
                        continue



def main():
    pages = [i for i in range(41, 51)]
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

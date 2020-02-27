import os
import cv2
import sys
path = "E:\zsm\TestResult701_1500noapk"
files = os.listdir(path)
normal_popup = open("C:\\Users\\GuoYi\\Desktop\\弹框\\popup.txt", "a")
liumang_popup = open("C:\\Users\\GuoYi\\Desktop\\流氓弹框\\popup.txt", "a")
normal_ads = open("C:\\Users\\GuoYi\\Desktop\\广告\\ads.txt", "a")
liumang_ads = open("C:\\Users\\GuoYi\\Desktop\\流氓广告\\ads.txt", "a")
fei = open("C:\\Users\\GuoYi\\Desktop\\正常界面\\jiemian.txt", "a")
sorted(files)
# print(len(files))
# print(files.index("700797"))
i = 0
for file in files[files.index("701453"):]:
    print("deal with " + file)
    pic_paths = os.path.join(path,file,"Screenshot")
    all_pics = os.listdir(pic_paths)
    for pic in all_pics:
        img = cv2.imread(os.path.join(pic_paths, pic))
        cv2.namedWindow(pic)
        cv2.moveWindow(pic, 50, 50)
        cv2.imshow(pic, cv2.resize(img,(0,0), fx=0.5, fy=0.5))
        cv2.waitKey(1)
        a = input()
        cv2.destroyWindow(pic)
        if a == '1':  # 正常弹框
            print("正常弹框")
            normal_popup.write(pic+'\n')
        elif a == '2': # 流氓弹框
            print("流氓弹框")
            liumang_popup.write(pic+'\n')
        elif a == '4':  # 正常广告
            print("正常广告")
            normal_ads.write(pic+'\n')
        elif a == '5':  # 流氓广告
            print("流氓广告")
            liumang_ads.write(pic+'\n')
        elif a== '0':
            fei.write(pic+'\n')
            print("正常界面")
        elif a=='7':
            normal_ads.close()
            normal_popup.close()
            liumang_popup.close()
            liumang_ads.close()
            fei.close()
            sys.exit(0)
        i += 1
        if i % 10 == 0:
            normal_ads.flush()
            normal_popup.flush()
            liumang_popup.flush()
            liumang_ads.flush()
            fei.flush()

normal_ads.close()
normal_popup.close()
liumang_popup.close()
liumang_ads.close()
fei.close()


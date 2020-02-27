import os
import cv2

path = "C:\\Users\\GuoYi\\Desktop\\zsm"
txt = os.path.join(path, "z1.txt")
pic = os.path.join(path, "z1.jpg")

img = cv2.imread(pic)
with open(txt, "r") as f:
    lines = f.readlines()

tag = False
kehui = False
for idx, line in enumerate(lines):
    line = line.strip()
    if "className:android.widget.ImageView" == line:
        tag = True
    if tag and "bounds:" in line:
        tag = False
        x = list(map(int, line.split(' ')[1].split(',')))
        kehui = True
    if "clickable" in line and kehui:
        kehui = False

        if line.split(':')[1] == 'true':
            color = (255, 0, 0)
        else:
            color = (0,0,255)
        cv2.rectangle(img, (x[0], x[1]), (x[2], x[3]), color, 2)

cv2.namedWindow("zsm", cv2.WINDOW_NORMAL)
cv2.imshow("zsm", img)
cv2.waitKey()

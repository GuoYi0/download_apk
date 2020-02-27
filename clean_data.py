import os
from IPython import embed


WIDTH, HEIGHT = 1080, 1920


path = "E:\\TestResult20191010"
files = os.listdir(path)
for file in files:
    f = os.path.join(path, file)
    popupinfo = os.path.join(f, "PopUpInfo")
    dd = os.listdir(popupinfo)
    for txt in dd:
        t = os.path.join(popupinfo, txt)
        embed()
        with open(t, 'r') as f:
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if "sequence" in line:
                pass



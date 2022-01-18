import pyautogui
from time import sleep
import pythoncom

def getData(s21,sum,time_start = "1900-01-01",time_end = "2099-12-31"):
    import pyperclip
    import pyscreeze
    import time

    pyautogui.moveTo(288, 1058)
    #pyautogui.click()
    pyautogui.moveTo(500,500)
    pyautogui.scroll(100000)

    x,y=pyscreeze.locateCenterOnScreen(r'C:\Users\21058\Desktop\image\clear.png',confidence=0.8)
    pyautogui.moveTo(x,y)
    pyautogui.click()
    sleep(2)
    pyautogui.scroll(10000)
    pyautogui.moveTo(545,438) #刑事案件
    pyautogui.click()
    sleep(3)

    pyautogui.moveTo(473,536) #高级检索
    pyautogui.click()
    pyautogui.moveTo(1077, 804) #时间
    pyautogui.click()
    pyperclip.copy(time_start)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('tab')
    pyperclip.copy(time_end)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.moveTo(594, 602)  # 搜索栏
    pyautogui.click()
    pyperclip.copy(s21)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.scroll(-500)
    pyautogui.moveTo(844,538) #检索
    pyautogui.click()
    pyautogui.scroll(100000)

    for i in range(sum):
        time.sleep(1)
        pyautogui.moveTo(1509, 832)
        pyautogui.click()
        pyautogui.moveTo(1743, 836)
        pyautogui.click()
        pyautogui.scroll(-100000)
        #time.sleep(1)
        x, y = pyscreeze.locateCenterOnScreen(r'C:\Users\21058\Desktop\image\nextpage.png', confidence=0.8)
        pyautogui.moveTo(x-120, y)
        # input()
        pyautogui.click()
        pyautogui.scroll(100000)


    return readWenShu()


def readWenShu():
    import os
    os.mkdir(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/doc")

    import time
    import zipfile
    from win32com import client as wc
    import docx
    import shutil
    pathdir = os.listdir(r"C:\Users\21058\Desktop\分词系统\Segmenter\Segmenter\download")
    zips = []

    for file in pathdir:
        zips.append(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/download/" + file)
    for zip in zips:
        z = zipfile.ZipFile(zip, 'r')
        z.extractall(path=r'C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/doc')
        z.close()
    pathdir = os.listdir(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/doc")


    for file in pathdir:
        pythoncom.CoInitialize()
        word = wc.Dispatch('Word.Application')
        if not file.endswith("doc") or " " in file:
            continue
        file = r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/doc/" + file
        try:
            doc = word.Documents.Open(file)  # 目标路径下的文件
            newfile = (file + "x").replace("doc/", "save/")
            doc.SaveAs(newfile, 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
            doc.Close()
            word.Quit()
            time.sleep(1)
            os.remove(file)
        except :
            continue

    shutil.rmtree(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/doc")


    result = ""
    already=0
    for file in os.listdir(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/save"):
        document = docx.Document("C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/save/" + file)
        passage = ""
        for paragraph in document.paragraphs:
            passage += paragraph.text
        if "ֈ" in passage or '你因' in passage or '你为' in passage:
            continue
        result += passage + "@"
    for file in os.listdir(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/save"):
        os.remove(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/save/" + file)
        del (file)
    for file in os.listdir(r"C:\Users\21058\Desktop\分词系统\Segmenter\Segmenter\download"):
        os.remove(r"C:/Users/21058/Desktop/分词系统/Segmenter/Segmenter/download/" + file)
    return result

# print(getData("李亚飞",4,"2016-01-01","2020-12-30",person="李亚飞"))


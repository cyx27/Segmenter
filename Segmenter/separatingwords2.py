from django.http import HttpResponse
from django.utils.encoding import escape_uri_path
from Model.models import Information
from django.shortcuts import render
import sys
# from signal import signal, SIGPIPE, SIG_DFL
import signal
import json
import jieba
import os
import jieba.posseg as pseg
from django.http import FileResponse
from django.http import StreamingHttpResponse
from Model.models import Datatext
from Model.models import Tempsave
import os


# 数据库操作
def seperate(request):
    # signal(SIGPIPE, SIG_DFL)
    def readFileAndPretreat(toDo):
        # with open(fileName, 'r+', encoding='utf-8') as f:
        # toDo = f.readlines()
        # toDo = "".join(toDo) + ""
        toDo = toDo.replace("（", "")
        toDo = toDo.replace("）", "")
        toDo = toDo.replace("、", "")
        toDo = toDo.replace(" ", "")
        toDo = toDo.replace("：", "")
        return toDo

    totry = Tempsave.objects.all()
    todotemp = ""
    for val in totry:
        todotemp += val.Content
    todo = readFileAndPretreat(todotemp)
    seg_list = pseg.cut(todo)
    seg_list = list(seg_list)

    name = ""
    gender = ""
    ethnicity = ""
    birthplace = ""
    accusation = ""
    courts = ""

    for i in range(len(seg_list)):
        # print(seg_list[i].word, seg_list[i].flag)
        # 存储姓名
        if name == "" and (
                seg_list[i].word == "被告人" or seg_list[i].word == "被告" or seg_list[i].word == "被执行人" or seg_list[
            i].word == "一审被告二审被上诉人" or seg_list[i].word == "罪犯"):
            temp = ""
            for j in range(i + 1, i + 11):
                if seg_list[j].flag != "x" and seg_list[j].word != "曾用名":
                    temp += seg_list[j].word
                else:
                    break
            if temp.startswith("单位"):
                temp = temp[2:]
            name = temp.strip()  # 存储姓名完

        # 存储民族
        if ethnicity == "" and seg_list[i].flag == "eth":
            ethnicity = seg_list[i].word

        # 存储性别
        if gender == "" and (seg_list[i].word == "男" or seg_list[i].word == "女"):
            gender = seg_list[i].word

        # 存储出生地
        if birthplace == "" and seg_list[i].word == "出生于":
            temp = ""
            for j in range(i + 1, len(seg_list)):
                if seg_list[j].flag != "x":
                    temp += seg_list[j].word
                else:
                    break
            birthplace = temp  # 存储出生地完

        # 存储没有顿号的罪名：可能多个罪名
        if seg_list[i].flag == "cri" and (seg_list[i].word not in accusation):
            if accusation == "":
                accusation += seg_list[i].word
            else:
                accusation += "，" + seg_list[i].word  # 存储没有顿号的罪名完

        if seg_list[i].flag == "toc" and (seg_list[i].word not in accusation):
            temp = seg_list[i].word
            for j in range(i + 1, i + 5):
                if seg_list[j].flag == "toc":
                    temp += "、" + seg_list[j].word
                elif seg_list[j].flag == "ncc":
                    if j == i + 1:
                        temp += "、" + seg_list[j].word
                    else:
                        temp += seg_list[j].word
                    break
            u = 0
            for u in range(0, len(temp)):
                if temp[u] == "罪":
                    break
            temp = temp[0:u + 1]
            if "罪" in temp:
                if accusation == "" or temp == "":
                    accusation += temp
                else:
                    accusation += " " + temp  # 存储有顿号的罪名完

        # 存储法院：可能多个法院
        if seg_list[i].flag == "cou" and (seg_list[i].word not in courts):
            if courts is "":
                courts += seg_list[i].word
            else:
                courts += "，" + seg_list[i].word  # 存储法院完

    if accusation.endswith(","):
        accusation = accusation[:-1]
    if len(name) >= 7:
        ethnicity = ""
        gender = ""
        birthplace = ""
    dic = {"Criminals": name, "Gender": gender, "Ethnicity": ethnicity, "Birthplace": birthplace,
           "Accusation": accusation,
           "Courts": courts}
    a = dic
    Information.objects.all().delete()
    test = Information(Criminals=a.get("Criminals"), Gender=a.get("Gender"), Ethnicity=a.get("Ethnicity"),
                       Birthplace=a.get("Birthplace"), Accusation=a.get("Accusation"), Courts=a.get("Courts"))
    test.save()
    listvar = Information.objects.all()
    # Information.objects.all().delete()
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    # list = TestInfo.objects.all()
    # 输出所有数据
    # response = list.get(Criminals="郑建国")
    context = {}
    val = ''
    if listvar:
        val = listvar[0]
    # context['rlt'] = request.POST['q']
    request.encoding = 'utf-8'
    if request.method == "GET":
        context['name'] = val.Criminals
        context['gender'] = val.Gender
        context['ethnicity'] = val.Ethnicity
        context['birthplace'] = val.Birthplace
        context['accusation'] = val.Accusation
        context['courts'] = val.Courts
        context['warning'] = '分词成功'
        list2 = Datatext.objects.all()
        result = ""
        context['alltext'] = []
        for val in totry:
            context['alltext'].append(val.Content)
        context['text'] = todotemp
    else:
        context['warning'] = '查无此人'
        context['name'] = ' '
        context['gender'] = " "
        context['ethnicity'] = " "
        context['birthplace'] = " "
        context['accusation'] = " "
        context['courts'] = " "
    return render(request, 'index2.html', context=context)


def download(request):
    """
    将字典对象保存为Json文件
    """
    # signal(SIGPIPE, SIG_DFL)
    request.encoding = 'utf-8'

    class SaveJson(object):

        def save_file(self, path, item):

            # 先将字典对象转化为可写入文本的字符串
            item = json.dumps(item, ensure_ascii=False)

            try:
                if not os.path.exists(path):
                    with open(path, "w", encoding='utf-8') as f:
                        f.write(item + "\n")
                else:
                    with open(path, "a", encoding='utf-8') as f:
                        f.write(item + "\n")
            except Exception as e:
                print("write error==>", e)

    s = SaveJson()
    list = Information.objects.all()
    dict = {}
    path = ""
    name = ""
    for val in list:
        dict = {"Criminals": val.Criminals, "Gender": val.Gender, "Ethnicity": val.Ethnicity,
                "Birthplace": val.Birthplace,
                "Accusation": val.Accusation,
                "Courts": val.Courts}
        path = "\\"
        path = path + val.Criminals + ".json"
        path = r"C:\Users\21058\Desktop\分词系统\Segmenter\json" + path
        name = val.Criminals

    with open(path, "w+", encoding="UTF-8") as f:
        f.seek(0)
        f.truncate()
    s.save_file(path, dict)
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    zys = "attachment;filename={}".format(escape_uri_path("对" + name + "裁判文书的标注.json"))
    response['Content-Disposition'] = zys
    file.close()
    os.remove(path)
    return response
    # file = open(path, 'rb')
    # file = open(path, 'rb')
    # response = FileResponse(file)
    # response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    # response['Content-Disposition'] = 'attachment;filename='+name
    # return

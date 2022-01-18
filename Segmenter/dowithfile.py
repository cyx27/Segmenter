# 开发时间:2021/11/28 14:22
# _*_coding:utf-8 _*_
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.encoding import escape_uri_path
from Segmenter import compare
from Model.models import Information
from Model.models import Datatext
from Model.models import Tempsave
import os


def upload(request):
    context = {}
    if request.method == "POST":
        # request.ContentType="text/html";
        files = request.FILES.get('myfile', None)
        result = ""
        for line in files.chunks():
            line = line.strip()
            result = result + str(line,encoding='utf-8')
        # Datatext.objects.all().delete()
        list1 = Datatext.objects.all()
        already=False
        count = len(list1)+1

        for i in range(0,len(list1)):
            print(compare.compare(result,list1[i].Content))
            if compare.compare(result,list1[i].Content)>=0.8:
                already=True
        if not already:
            test = Datatext(Id=count, Content=result)
            test.save()
        #list2 = Datatext.objects.all()
        context['alltext'] = []
        context['alltext'].append(result)
        # for var in list2:
        #     if len(var.Content) != 0:
        #         context['alltext'].append(var.Content)
        #         count += 1
    # return HttpResponse(request.FILES+"123")
    return render(request, 'index3.html', context=context)


def download(request):
    if request.method == "GET":
        list1 = Tempsave.objects.all()
        val = list1[0]
        rootpath = r'C:\Users\21058\Desktop\分词系统\Segmenter\txt'
        path = "\\"
        path = path + "案例文书" + ".txt"
        with open(rootpath + path, "w+", encoding="UTF-8") as f:
            f.seek(0)
            f.truncate()
            f.write(val.Content)
            f.close()
        file = open(rootpath + path, 'rb')
        response = HttpResponse(file)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        zys = "attachment;filename={}".format(escape_uri_path("案例文书.txt"))
        response['Content-Disposition'] = zys
        file.close()
        os.remove(rootpath+path)
        return response

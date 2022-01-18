from django.http import HttpResponse
from django.shortcuts import render
from Model.models import Information
from Model.models import Datatext
from Model.models import Tempsave
#from signal import signal, SIGPIPE, SIG_DFL
import signal

def index(request):
    #signal(SIGPIPE, SIG_DFL)
    list=Information.objects.all()
    # context={
    #     'post':list
    # }
    context={}
    if request.POST and list and request.POST['name']:
        # val.Criminals=request.POST['name']
        # val.Gender=request.POST['gender']
        # val.Ethnicity=request.POST['ethnicity']
        # val.Birthplace=request.POST['birthplace']
        # val.Accusation=request.POST['accusation']
        # val.Courts=request.POST['courts']
        # val.save()
        Information.objects.all().delete()
        test = Information(Criminals=request.POST['name'], Gender=request.POST['gender'], Ethnicity=request.POST['ethnicity'],
                           Birthplace=request.POST['birthplace'], Accusation=request.POST['accusation'], Courts=request.POST['courts'])
        test.save()
        context['name'] = test.Criminals
        context['gender'] = test.Gender
        context['ethnicity'] = test.Ethnicity
        context['birthplace'] = test.Birthplace
        context['accusation'] = test.Accusation
        context['courts'] = test.Courts
        context['warning'] = '修改成功'
        list2 = Datatext.objects.all()
        context['alltext'] = []
        for val in list2:
            context['alltext'].append(val.Content)
        totry = Tempsave.objects.all()
        todotemp = ""
        for val in totry:
            todotemp += val.Content
        context['text'] = todotemp
    # 输出所有数据
    return render(request, 'index3.html', context=context)

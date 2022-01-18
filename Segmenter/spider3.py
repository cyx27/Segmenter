from django.http import HttpResponse
from django.shortcuts import render
from Model.models import Information
from Model.models import Datatext
from Model.models import Tempsave
from Segmenter import wenshu_requests
def spider(request):
    text=""
    context={}
    # if request.GET:
    #     text=wenshu_requests.getData(request.GET['key'],int(request.GET['number']),str(request.GET['start']),str(request.GET['stop']))
    #     Datatext.objects.all().delete()
    #     list=text.split("@")
    #     count=1
    #     context['alltext'] = []
    #     for var in list:
    #         if len(var)!=0 and str(request.GET['key']) in var:
    #             test=Datatext(Id=count,Content=str(count)+var)
    #             test.save()
    #             context['alltext'].append(str(count) + var)
    #             count+=1

    if request.POST:
        list2 = Datatext.objects.all()
        result=""
        context['alltext'] = []
        index = request.POST['datatext']
        for val in list2:
            # if not index[1].isdigit():
            #     index = index[0]
            # if int(index)==val.Id:
            if index in val.Content:
                print(val.Content)
                print(index)
                print(1)
                result+=val.Content
                Tempsave.objects.all().delete()
                test=Tempsave(Content=val.Content)
                test.save()
                context['alltext'].append(val.Content)
        context['text'] = result

    return render(request, 'index3.html', context=context)
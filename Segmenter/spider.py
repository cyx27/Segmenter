from django.http import HttpResponse
from django.shortcuts import render
from Model.models import Information
from Model.models import Datatext
from Model.models import Tempsave
from Segmenter import wenshu_requests
import time
def spider(request):
    text=""
    context={}
    if request.GET:
        already=0
        need = int(request.GET['number'])*4
        #test = Datatext(Content="this is a test", Keywords="傻逼",Unique="this is a test")
        # Datatext.objects.get_or_create(Content="this is a test", Keywords="傻逼",Unique="this is a test")
        # #test.save()
        # Datatext.objects.get_or_create(Content="this is a test2", Keywords="傻逼", Unique="this is a test2")
        # #test.save()
        # Datatext.objects.get_or_create(Content="this is a test3", Keywords="傻逼",Unique="this is a test3")
        # #test.save()
        # Datatext.objects.get_or_create(Content="this is a test4", Keywords="傻逼",Unique="this is a test4")
        # #test.save()
        have = Datatext.objects.all().filter(Keywords=str(request.GET['key']))
       # have = Datatext.objects.all().filter(Content=str(request.GET['key']))
        print(have)
        #input("continue..")
        context['alltext'] = []
        #and str(request.GET['key']) in var
        for val in have:
            var=val.Content
            if len(var) != 0:
                already+=1
                context['alltext'].append(var)
            if already == need:
                return render(request, 'index.html', context=context)
        text=wenshu_requests.getData(request.GET['key'],int(request.GET['number']),str(request.GET['start']),str(request.GET['stop']))
        #Datatext.objects.all().delete()
        list=text.split("@")
        count=1

        for var in list:
            if len(var)!=0 and str(request.GET['key']) in var:
                #test=Datatext(Id=count,Content=var,Keywords=str(request.GET['key']))
                Datatext.objects.get_or_create(Content=var, Keywords=str(request.GET['key']), Unique=var[0:199])
               # test.save()
                context['alltext'].append(var)
                count+=1
        # try:
        #     have = Datatext.objects.all().filter(Keywords=str(request.GET['key']))
        #     needstartime=str(request.GET['start']).split("-")
        #     needovertime=str(request.GET['stop']).split("-")
        #     for val in have:
        #         if already==need:
        #             break
        #         startime=val.StartTime.split("-")
        #         overtime = val.OverTime.split("-")
        #         if int(startime[0]+startime[1]+startime[2])>=int(needstartime[0]+needstartime[1]+needstartime[2]):
        #             if int(overtime[0]+overtime[1]+overtime[2])<=int(needovertime[0]+needovertime[1]+needovertime[2]):
        #                 already+=1
        # except:pass
        # if already<need:
        #     text = wenshu_requests.getData(request.GET['key'], int(request.GET['number']), str(request.GET['start']),
        #                                    str(request.GET['stop']))
        #     list=text.split("@")
        #     count=1
        #     all=len(Datatext.objects.all())+1
        #     context['alltext'] = []
        #     #Datatext.objects.all().delete()
        #     for var in list:
        #         if len(var)!=0 and str(request.GET['key']) in var:
        #             test=Datatext(Id=all,Content=str(count)+var,Keywords=str(request.GET['key']),StartTime=str(request.GET['start']),OverTime=str(request.GET['stop']))
        #             test.save()
        #             context['alltext'].append(str(count) + var)
        #             count+=1
        #             all+=1
        #             if count-1==need:
        #                 break
        # else:
        #     count = 1
        #     already=0
        #     context['alltext'] = []
        #     for val in have:
        #         if already == need:
        #             break
        #         context['alltext'].append(str(val.Content))
        #         count += 1
        #         already+=1
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
                result+=val.Content
                Tempsave.objects.all().delete()
                test=Tempsave(Content=val.Content)
                test.save()
        context['alltext'].append(val.Content)
        context['text'] = result

    return render(request, 'index.html', context=context)
from django.http import HttpResponse
from django.shortcuts import render
from Model.models import Information
from Model.models import Datatext
from Model.models import Tempsave
from Segmenter import searchcourt
def spider(request):
    text = ""
    context = {}
    if request.GET:
        already = 0
        need = int(request.GET['number']) * 4
        have = Datatext.objects.all().filter(Courts=str(request.GET['key']))
        print(have)
        #input("continue..")
        context['alltext'] = []
        for val in have:
            var = val.Content
            if len(var) != 0 and str(request.GET['key']) in var:
                already += 1
                context['alltext'].append(var)
            if already == need:
                return render(request, 'index2.html', context=context)
        text = searchcourt.getData(request.GET['key'], int(request.GET['number']), str(request.GET['start']),
                                       str(request.GET['stop']))
        list = text.split("@")
        count = 1

        for var in list:
            if len(var) != 0 and str(request.GET['key']) in var:
                Datatext.objects.get_or_create(Content=var, Criminal=str(request.GET['key']), Unique=var[0:199])
                context['alltext'].append(var)
                count += 1

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

    return render(request, 'index2.html', context=context)
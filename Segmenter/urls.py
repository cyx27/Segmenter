"""Segmenter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import index,separatingwords,spider,dowithfile,index1,index2,index3,spider1,spider2,spider3,separatingwords1,separatingwords2,separatingwords3
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',index.index),
    path('seperate/', separatingwords.seperate),
    path('download/', separatingwords.download),
    path('seperate1/', separatingwords1.seperate),
    path('download1/', separatingwords1.download),
    path('seperate2/', separatingwords2.seperate),
    path('download2/', separatingwords2.download),
    path('seperate3/', separatingwords3.seperate),
    path('download3/', separatingwords3.download),
    path('spider/',spider.spider),
    path('spider1/', spider1.spider),
    path('spider2/', spider2.spider),
    path('spider3/', spider3.spider),
    path('', index.index),
    path('upload/',dowithfile.upload),
    path('downloadfile/',dowithfile.download),
    path('index1/',index1.index),
    path('index2/',index2.index),
    path('index3/',index3.index),
]

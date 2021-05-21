"""testweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from nihao import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index),
    path('login/', views.user_login),
    path('', views.home),
    path('homeword-L2/', views.homeword_list),
    path('homeword/<title>', views.homeword),
    path('download/<id>', views.download_file),
    path('download/', views.download),
    path('register/', views.register),
    path('userinfo/', views.userinfo),
    path('logout/', views.logout),
    path('test/',views.test),
    path('words_number/',views.words_number),
    path('wechat/',views.wechat),
    path('homeword-L3/',views.homewordL3),
    path('api/',views.api)

]

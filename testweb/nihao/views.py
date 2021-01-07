from django.shortcuts import render, HttpResponse, redirect
from HomeWord import Homeword_spider
from nihao.forms import CustoFrom
import time
import os
# import zmail


# Create your views here.
def index(request):
    if request.method == "GET":
        return render(request, "index.html", {"method": request.method})
    elif request.method == "POST":
        form = CustoFrom(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["user"]
            pwd = form.cleaned_data["pwd"]
            # username = request.POST.get("username")
            # pwd = request.POST.get("pwd")
            zjh = Homeword_spider.HomeWord(username, pwd)
            zjh.login()
            return render(request, "index.html", {"datetime": zjh.homeword_count(), "method": request.method})
        else:
            return render(request, "index.html", {"form": form})


def home(request):
    return redirect("/index")


def login(request):
    if request.method == "POST":
        return HttpResponse("哈哈哈哈")
    elif request.method == "GET":
        return HttpResponse("。。。。。。。。。。。")


def homeword(request):
    if request.method == "GET":
        return render(request, "homeword.html")

    elif request.method == "POST":
        info = request.POST.get("answer")

        time_info = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
        path = "作业/{}".format(time_info)
        os.makedirs(path, exist_ok=True)
        with open(path + "/陈泽南作业.txt", "w", encoding="utf-8") as f:
            f.write(info)


        # MAIL = {
        #     "subject": time_info+"陈泽南作业！",
        #     "content_text": info
        # }
        # server = zmail.server("guishoushi126@126.com", "zten880")
        # server.send_mail("zhangjianhang@xiaoma.cn", MAIL)
        # print("发送成功")

        return HttpResponse("作业提交成功！")

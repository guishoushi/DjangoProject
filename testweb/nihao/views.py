from django.shortcuts import render, HttpResponse, redirect
from HomeWord import Homeword_spider, WeChat
from nihao.forms import CustoFrom, LoginFrom
from nihao.models import UserInfo, HomeWord
from markdown import markdown

import time
import os


# import zmail


# Create your views here.
def index(request):
    if request.method == "GET":
        if not is_login(request):
            return redirect("/login")

        return render(request, "index_test.html", locals())


def api(request):
    # url = 'http://wthrcdn.etouch.cn/weather_mini?city=上海'
    # res = requests.get(url).text

    return HttpResponse('<img>  我是测试 </img>')


def words_number(request):
    if not is_login(request):
        return redirect("/login")

    if request.method == "GET":
        return render(request, "index.html")
    if request.method == "POST":
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


def wechat(request):
    if not is_login(request):
        return redirect('/login')

    if request.method == "GET":
        return render(request, "wechat.html")
    if request.method == "POST":
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        number = request.POST.get("number")
        info = WeChat.main(phone, password, number)
        return render(request, 'wechat.html', locals())


def test(request):
    if not is_login(request):
        return redirect("/login")
    if request.method == "GET":
        title = HomeWord.objects.filter(type=2)
        print(title)
        return HttpResponse(content=title)


def is_login(request):
    """
    判断session是否存在用户名
    用来判断用户是否登录
    :param request:
    :return:
    """
    try:
        if request.session._session["name"]:
            pass
    except Exception as e:
        return False

    else:
        return True


def home(request):
    if not is_login(request):
        return redirect("/login")
    return redirect("/index")


def userinfo(request):
    if not is_login(request):
        return redirect("/login")

    return render(request, "userinfo.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            is_username = UserInfo.objects.get(username=username)
        except Exception as e:
            return render(request, "login.html", {"is_username": "用户不存在，请先注册！"})
        else:
            if is_username.password == password:
                request.session["name"] = username
                res = redirect('/index')
                res.set_cookie("is_Login", True, 60 * 60 * 24 * 7)
                res.set_cookie('username', username.encode())
                return res
            else:
                return render(request, "login.html", {"is_password": "密码错误，请输入正确密码！"})


    elif request.method == "GET":
        if not is_login(request):
            return render(request, "login.html")
        return redirect('/index')


def logout(request):
    """
    退出用户函数清空请求session
    :param request:
    :return:
    """
    request.session.flush()
    return redirect("/login")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    if request.method == "POST":
        form = LoginFrom(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password1 = form.cleaned_data["password1"]
            password2 = form.cleaned_data["password2"]
            is_username = UserInfo.objects.filter(username=username)
            if is_username:
                return render(request, "register.html", context={"is_username": "用户名已存在！"})
            else:
                if password1 == password2:
                    UserInfo.objects.create(username=username, password=password1, email=email)
                    return redirect("/login")
                else:
                    return render(request, "register.html", context={"pwd_error": "两次密码不一致！"})
        else:
            return render(request, "register.html", context={"form": form})


def homeword_list(request):
    if not is_login(request):
        return redirect("/login")

    if request.method == "GET":
        title = HomeWord.objects.filter(type=2).order_by('-title')
        return render(request, "homeword_list.html", locals())

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


def homewordL3(request):
    if not is_login(request):
        return redirect("/login")
    if request.method == "GET":
        title = HomeWord.objects.filter(type=3)
        print(title)
        return render(request, 'homeword_list.html', locals())


def homeword(request, title):
    if not is_login(request):
        return redirect("/login")
    if request.method == "GET":
        try:
            title = HomeWord.objects.get(title=title)
        except:

            return redirect("/index")
        else:
            # return HttpResponse(word)

            return HttpResponse(markdown(title.wordinfo))

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

        return HttpResponse("作业提交成功了！")


def download(request, ):
    if not is_login(request):
        return redirect("/login")
    if request.method == "GET":
        items = os.listdir(os.getcwd() + "/static/file")
        # with open("static/file/pycryptodome_AES加密文档.pdf", "rb") as f:
        #     f1 = f.read()
        # response = HttpResponse(f1)
        # response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        # response['Content-Disposition'] = 'attachment;filename="AES.pdf"' # 设置文件名字
        # return response
        return render(request, "download.html", {"items": items})


def download_file(request, id):
    if not is_login(request):
        return redirect("/login")
    if request.method == "GET":
        with open("static/file/{}".format(id), "rb") as f:
            f1 = f.read()
        response = HttpResponse(f1)
        response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
        response['Content-Disposition'] = 'attachment;filename="{}"'.format(id)  # 设置文件名字
        return response

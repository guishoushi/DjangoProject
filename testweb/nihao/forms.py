"""
·座右铭：怕蛇的人不用Python
·Project：DjangoProject
·Author：张建行
·File：froms
·IDE：PyCharm
·Time：2021-01-05 18:53
"""
from django import forms


class CustoFrom(forms.Form):
    user = forms.IntegerField(label="账号：")
    pwd = forms.CharField(label="密码：")

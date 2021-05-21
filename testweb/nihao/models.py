from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(max_length=10, verbose_name="用户名")
    password = models.CharField(max_length=20, verbose_name="密码")
    email = models.EmailField(null=False, verbose_name="邮箱")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户名"
        verbose_name_plural = verbose_name
        db_table = "User"


class HomeWord(models.Model):
    title = models.CharField(max_length=40, verbose_name="家庭作业")
    wordinfo = models.TextField(max_length=21845, verbose_name="作业内容")
    type = models.IntegerField(max_length=10, verbose_name='课程类型')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "家庭作业"
        verbose_name_plural = "家庭作业"
        db_table = "HomeWord"

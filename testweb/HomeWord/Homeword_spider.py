"""
·座右铭：怕蛇的人不用Python
·Project：HomeWord
·Author：张建行
·File：Homeword_spider
·IDE：PyCharm
·Time：2021-01-03 22:39
"""
import requests, json


class HomeWord(object):
    def __init__(self, username, password):
        self.login_url = "https://classroom-courseapi.xiaomawang.com/v1/user/login"
        self.data = {"username": username, "password": password}
        self.session = requests.Session()
        self.headers = {"PermissionSetId": "1724", "Access-Token": ""}
        self.class_info_dict = {}
        self.ok_homeword_number = 0
        self.json_info = {}
        self.lessonList = []

    def login(self):
        res = self.session.post(url=self.login_url, data=self.data).json()
        if res["message"] != "操作成功":
            # print("登录失败！无法获得token！")
            self.json_info["message"] = "登录失败！无法获得token！"
            return self.json_info
        else:
            # print("登录成功！已获得token！")
            self.json_info["message"] = "登录成功！已获得token！"
            self.headers["Access-Token"] = res["data"]["token"]
            class_res = self.session.get(
                "https://classroom-courseapi.xiaomawang.com/v1/class/list?status=1&page=1&limit=20",
                headers=self.headers).json()
            if class_res["message"] != "操作成功":
                # print("获得班级信息失败！")
                self.json_info["ClassInfo"] = ["获得班级信息失败！"]
            else:
                class_list = class_res["data"]["list"]
                class_list = [i["classId"] for i in class_list if i["courseName"] != "Python3.0(L1)"]
                self.parse_class_info(class_list)

    def parse_class_info(self, class_list):

        for id in class_list:
            class_info = self.session.get(
                "https://classroom-courseapi.xiaomawang.com/v1/lesson/get-process-list?classId={}&page=1&limit=80".format(
                    id), headers=self.headers).json()
            if class_info["message"] != "操作成功":
                # print("获取课程列表失败！")
                self.json_info["LessonList"] = "获取课程列表失败！"
            else:
                class_info_list = [i["lessonId"] for i in class_info["data"]["list"] if i["lessonStatus"] == 1][-2]
                self.class_info_dict[id] = class_info_list

    def homeword_count(self):
        for key, value in self.class_info_dict.items():
            homeword = self.session.get(
                "https://classroom-courseapi.xiaomawang.com/v1/homework/get-class-homework?classId={}&lessonId={}".format(
                    key, value),
                headers=self.headers).json()
            if homeword["message"] != "操作成功":
                # print("获取作业人数数据失败！")
                self.json_info["HomeWord"] = "获取作业人数数据失败！"
            else:
                self.ok_homeword_number += len(homeword["data"]["studentList"])
                # print(homeword["data"]["lessonName"] + "完成人数为：", len(homeword["data"]["studentList"]))
                self.lessonList.append({"lessonName": homeword["data"]["lessonName"],
                                        "ok_number": len(homeword["data"]["studentList"])})

        # print("共完成{}人！\nPythonL1、C++课程不在统计范围之内！".format(self.ok_homeword_number))
        self.json_info["ok_homeword_number"] = self.ok_homeword_number
        self.json_info["LessonList"] = self.lessonList
        # self.json_info = json.dumps(self.json_info)
        return self.json_info


# zjh = HomeWord(12246, "zten880F")
# class_list = zjh.login()

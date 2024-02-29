# import pymysql
import sqlite3
import copy

from tracker.requirement import Requirement
from tracker.course import Course

import pandas as pd

class Student:
    def __init__(self, id, name, department, major, grade):
        self.id = id
        self.name = name
        self.department = department
        self.major = major
        self.grade = grade

        self.requirement = Requirement("courses/网络空间安全.json")

        self.my_progress = {}
        self.my_progress_detail = {}
        for key in self.requirement.get_core_category():
            self.my_progress[key] = 0
            self.my_progress_detail[key] = []

        self.my_progress_other = {}
        self.my_progress_other_detail = {}
        for key in self.requirement.get_other_category():
            self.my_progress_other[key] = 0
            self.my_progress_other_detail[key] = []

        self.my_courses = []
        self.maybe_english_courses = []
        self.maybe_general_or_art_courses = []

    def add_progress(self, category, credit, course):
        self.my_progress[category] += credit
        self.my_progress_detail[category].append(course.name + "(" + str(course.credit) + "学分" + ")")

    def add_progress_other(self, category, credit, course):
        self.my_progress_other[category] += credit
        self.my_progress_other_detail[category].append(course.name + "(" + str(course.credit) + "学分" + ")")

    def print_progress(self):
        print("========= 基础学分要求 =========")
        for key in self.my_progress:
            print(key, self.my_progress[key])

        print("========= 其他学分要求 =========")
        for key in self.my_progress_other:
            print(key, self.my_progress_other[key])


    def get_progress(self):
        res = []
        print(len(self.maybe_general_or_art_courses))
        for i in range(2 ** len(self.maybe_general_or_art_courses)):
            my_progress = copy.deepcopy(self.my_progress)
            my_progress_detail = copy.deepcopy(self.my_progress_detail)
            my_progress_other = copy.deepcopy(self.my_progress_other)
            my_progress_other_detail = copy.deepcopy(self.my_progress_other_detail)
            info = ''
            condition = bin(i)[2:]
            for index, cond in enumerate(condition[::-1]):
                course = self.maybe_general_or_art_courses[index]
                # 表示为核通
                if cond == "0":
                    my_progress["素质教育通识限修课"] += course.credit
                    my_progress_detail["素质教育通识限修课"].append(course.name + "(" + str(course.credit) + "学分" + ")")

                    info += self.maybe_general_or_art_courses[index].name + "(核通)  "
                # 表示为美育
                else:
                    my_progress["素质教育理论必修课"] += course.credit
                    my_progress_detail["素质教育理论必修课"].append(course.name + "(" + str(course.credit) + "学分" + ")")
                    info += self.maybe_general_or_art_courses[index].name + "(美育)  "

            res.append((info, my_progress, my_progress_detail, my_progress_other, my_progress_other_detail))

        return res


    def read_my_courses(self, path):
        data = pd.read_excel(path)
        vaild_courses_dict = {}
        for index, row in data.iterrows():
            # 读取课程编号
            course_id = row["课程代码"]
            # 读取课程名称
            name = row["课程名称"]
            # 读取课程学分
            credit = row["学分"]
            # 读取课程开设单位
            department = row["承担单位"]
            # 读取课程类别
            course_type = row["课程类别"]
            course_type = "外语类" if course_type == "语言类" else course_type

            if course_type == "思政、军理类":
                if "军事" in name:
                    course_type = "军理类"
                else:
                    course_type = "思政类"

            # 是否通过
            passed = True if row["是否及格"] == "是" else False

            c = Course(course_id, name, department, credit, category=course_type)

            if passed:
                if vaild_courses_dict.get(course_id) is None:
                    vaild_courses_dict[course_id] = 1

                    self.my_courses.append(c)

                else:
                    continue

    def update_course_from_database(self):
        # 连接数据库
        # conn = pymysql.connect(host='localhost', user='coursemaster', password='coursemasterpasswd',
        #                        database='coursedb', charset='utf8')
        # 创建游标
        # c = conn.cursor()

        conn = sqlite3.connect('./tracker/course.db')
        c = conn.cursor()

        # 查询
        for index, course in enumerate(self.my_courses):
            # c.execute('select * from course where id=%s', course.id)
            c.execute(f'select * from course where id="{course.id}"')
            # 获取查询结果
            result = c.fetchone()
            if result is None:
                continue
            else:
                category = result[5] if result[5] is not None else ""

                category = "外语类" if category == "语言类" else category
                if category == "思政、军理类":
                    if "军事" in course.name:
                        category = "军理类"
                    else:
                        category = "思政类"

                label = result[6] if result[6] is not None else ""
                language = result[7] if result[7] is not None else ""
                self.my_courses[index].category = category
                self.my_courses[index].label = label
                self.my_courses[index].language = language

        # 关闭游标
        c.close()
        # 关闭数据库连接
        conn.close()

    def analyze_my_progress(self):
        direct_types = ['数学与自然科学类', '工程基础类', '外语类', '思政类', '军理类', '体育类', '素质教育理论必修课',
                        '素质教育实践必修课']
        core_general = self.requirement.core_requirement["素质教育通识限修课"]["courses"]
        core_major = self.requirement.core_requirement["核心专业类"]["courses"]
        non_core_major = self.requirement.core_requirement["一般专业类"]["courses"]

        def is_art_course(course):
            if "美育" in course.label or course.id in self.requirement.art_courses:
                return True
            return False

        for course in self.my_courses:
            if course.category in direct_types:
                self.add_progress(course.category, course.credit, course)
            elif course.id in core_major:
                self.add_progress("核心专业类", course.credit, course)
            elif course.id in non_core_major:
                self.add_progress("一般专业类", course.credit, course)
            elif course.name == "科研课堂":
                self.add_progress("核心专业类", course.credit, course)
            elif course.id in core_general:
                self.add_progress("素质教育通识限修课", course.credit, course)
            else:
                self.maybe_english_courses.append(course)
                if course.category == "一般通识类" and is_art_course(course):
                    self.add_progress("素质教育理论必修课", course.credit, course)
                    print("美育 >>> ", course)
                elif course.category == "核心通识类" and not is_art_course(course):
                    self.add_progress("素质教育通识限修课", course.credit, course)
                    print("核心通识 >>> ", course)
                elif course.category == "核心通识类" and is_art_course(course):
                    self.maybe_general_or_art_courses.append(course)
                    print("核通美育待分配课程 >>> ", course)
                else:
                    print("未知课程 >>> ", course)

    def analyze_my_progress_other(self):

        # 劳育课
        for course in self.my_courses:
            if "劳育" in course.label or course.id in self.requirement.lab_courses.keys():
                self.add_progress_other("劳育课",
                                        self.requirement.lab_courses[course.id] if course.id in self.requirement.lab_courses.keys() else 16,
                                        course)

        # 创新创业课
        for course in self.my_courses:
            if "创新创业" in course.label or course.id in self.requirement.innovation_courses:
                self.add_progress_other("创新创业课", course.credit, course)

        # 跨专业课
        core_major = self.requirement.core_requirement["核心专业类"]["courses"]
        non_core_major = self.requirement.core_requirement["一般专业类"]["courses"]
        for course in self.my_courses:
            if "专业" in course.category:
                if course.id not in core_major and course.id not in non_core_major and course.name != "科研课堂":
                    self.add_progress_other("跨专业课", course.credit, course)

    def analyze_english_courses(self, english_courses):
        for course in self.my_courses:
            if course.name in english_courses:
                self.add_progress_other("全英课", course.credit, course)


if __name__ == "__main__":
    stu = Student("2020000001", "张三", "计算机学院", "网络空间安全", "2018")
    stu.read_my_courses("../全部成绩查询.xlsx")
    stu.update_course_from_database()

    stu.analyze_my_progress()
    stu.analyze_my_progress_other()
    stu.print_progress()




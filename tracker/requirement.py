import json
import pandas as pd

class Requirement:
    def __init__(self, path):
        self.path = path

        f = open(path, "r", encoding="utf-8")
        data = json.load(f)
        f.close()
        self.department = data["school"]
        self.major = data["major"]
        self.core_requirement = data["core_category"]
        self.other_requirement = data["other_category"]

        # 加载美育课
        self.art_courses = []
        data = pd.read_excel("courses/meiyu.xlsx")
        for index, row in data.iterrows():
            self.art_courses.append(row["课程代码"])

        # 加载劳育课
        self.lab_courses = {}
        data = pd.read_excel("courses/laoyu.xlsx")
        for index, row in data.iterrows():
            if pd.isna(row["课程代码"]):
                continue
            ids = str(row["课程代码"]).split("\n")
            for id in ids:
                self.lab_courses[id] = row["可认定的劳动教育学时"]

        # 加载创新创业课
        self.innovation_courses = []
        data = pd.read_excel("courses/chuangxinchuangye.xlsx")
        for index, row in data.iterrows():
            self.innovation_courses.append(row["课程代码"])


    def get_core_category(self):
        return list(self.core_requirement.keys())

    def get_other_category(self):
        return list(self.other_requirement.keys())

if __name__ == "__main__":
    requirement = Requirement("courses/网络空间安全.json")
    print(requirement.get_core_category())
    print(requirement.get_other_category())
    print(requirement.art_courses)
    print(requirement.lab_courses)
    print(requirement.innovation_courses)





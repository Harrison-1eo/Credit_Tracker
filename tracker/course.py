class Course:
    def __init__(self, id, name, department, credit, category="", label="", language=""):
        self.id = id
        self.name = name
        self.department = department
        self.credit = credit
        self.category = category
        self.label = label
        self.language = language

    def __str__(self):
        return f'课程编号：{self.id}, 课程名称：{self.name}, 学分：{self.credit}, 课程类别：{self.category}, 课程标签：{self.label}, 授课语言：{self.language}'

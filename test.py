from tracker.student import Student

stu = Student("2020000001", "张三", "网络空间安全学院", "网络空间安全", "2021")
stu.read_my_courses("全部成绩查询.xlsx")
stu.update_course_from_database()

stu.analyze_my_progress()
stu.analyze_my_progress_other()
stu.print_progress()

for course in stu.maybe_english_courses:
    print(course)

res = stu.get_progress()
for r in res:
    print(r)



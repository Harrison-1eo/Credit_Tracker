from flask import Flask, render_template, request, session
from tracker.student import Student
import random
import os

app = Flask(__name__)
app.secret_key = '24&o0-1!@#'


@app.template_filter('enumerate')
def _enumerate(iterable, start=0):
    return enumerate(iterable, start)


def process(path, major):
    # 处理上传文件和选项
    stu = Student("2020000001", "张三", "网络空间安全学院", "网络空间安全", "2021")
    stu.read_my_courses(path)
    stu.update_course_from_database()

    stu.analyze_my_progress()
    stu.analyze_my_progress_other()
    stu.print_progress()

    return stu, None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload():
    # 处理上传文件和选项
    file = request.files['file']
    major = request.form['major']

    # 检查是否存在uploads文件夹
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    path = 'uploads/' + file.filename + str(random.randint(0, 10000000))
    file.save(path)

    stu, _ = process(path, major)
    session['stu_path'] = path
    session['major'] = major

    courses = [(c.name, c.language) for c in stu.maybe_english_courses]
    return render_template('checkEnglish.html', courses=courses)


@app.route('/confirm', methods=['POST'])
def show_res():
    selected_english_courses = request.form.getlist('selected_courses')
    if 'stu_path' in session:
        stu, _ = process(session['stu_path'], session['major'])

        stu.analyze_english_courses(selected_english_courses)
        requirements = [0, stu.requirement.core_requirement, 0, stu.requirement.other_requirement]
        results = stu.get_progress()

        return render_template('result.html', results=results, requirements=requirements)
    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)

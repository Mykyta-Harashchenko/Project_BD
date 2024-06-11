import sqlite3
from datetime import datetime, date, timedelta
from faker import Faker
from random import randint

disciplines = ['Вища математика', 'Дискретна математика', 'Лінійна алгебра', 'Теорія імовірності', 'Статистика',
               'Математичний аналіз', 'Програмування']
groups = ['ПМ-22-1', 'ПМ-22-2', 'ПМ-22-3']
NUMBER_TEACHERS = 5
NUMBER_STUDENTS = 50
fake = Faker('uk_UA')
connect = sqlite3.connect('database.db')
cur = connect.cursor()


def seed_teachers():
    teachers = [fake.name() for _ in range(NUMBER_TEACHERS)]
    sql = "INSERT INTO teachers(fullname) VALUES(?);"
    cur.executemany(sql, zip(teachers, ))


def seed_disciplines():
    sql = "INSERT INTO subjects(subject_name, teacher_id) VALUES(?, ?);"
    cur.executemany(sql, zip(disciplines, iter(randint(1, NUMBER_TEACHERS) for _ in range(len(disciplines)))))


def seed_groups():
    sql = "INSERT INTO groups(name) VALUES(?);"
    cur.executemany(sql, zip(groups, ))


def seed_students():
    students = [fake.name() for _ in range(NUMBER_STUDENTS)]
    sql = "INSERT INTO students(fullname, group_id) VALUES(?, ?);"
    cur.executemany(sql, zip(students, iter(randint(1, len(groups)) for _ in range(len(students)))))


def seed_grades():
    start_date = datetime.strptime('2023-03-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-06-29', '%Y-%m-%d')
    sql = "INSERT INTO marks(subject_id, student_id, mark, date_of) VALUES(?, ?, ?, ?);"

    def get_list_dates(start: date, end: date):
        result = []
        current_date = start
        while current_date <= end:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result

    list_dates = get_list_dates(start_date, end_date)

    grades = []
    for day in list_dates:
        random_discipline = randint(1, len(disciplines))
        random_students = [randint(1, NUMBER_STUDENTS) for _ in range(5)]
        for student in random_students:
            grades.append((random_discipline, student, randint(1, 12), day.date()))
    cur.executemany(sql, grades)
"""---------------------------------------------------------------Requests--------------------------------------------------------------------"""
def find_top_students():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT students.fullname, AVG(marks.mark) as avg_mark
            FROM students
            JOIN marks ON students.id = marks.student_id
            GROUP BY students.id
            ORDER BY avg_mark DESC
            LIMIT 5;
        """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def find_top_student_by_subject(subject_name):
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT students.fullname, AVG(marks.mark) as avg_grade
            FROM students
            JOIN marks ON students.id = marks.student_id
            JOIN subjects ON marks.subject_id = subjects.id
            WHERE subjects.subject_name = ?
            GROUP BY students.id
            ORDER BY avg_grade DESC
            LIMIT 1;
        """
        cur.execute(query, (subject_name,))
        top_student = cur.fetchone()
        return top_student

def average_in_groups(subject_name):
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
                SELECT groups.name, AVG(marks.mark) AS avg_grade
                FROM marks
                JOIN students ON marks.student_id = students.id
                JOIN groups ON students.group_id = groups.id
                JOIN subjects ON marks.subject_id = subjects.id
                WHERE subjects.subject_name = ?
                GROUP BY groups.name;
                """
        cur.execute(query, (subject_name,))
        results = cur.fetchall()
        return results

def all_marks_average():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
                SELECT AVG(marks.mark) AS avg_grade
                FROM marks
                """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def courses_for_teachers():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT subjects.subject_name
            FROM subjects
            JOIN teachers ON subjects.teacher_id = teachers.id
            WHERE teachers.fullname = 'Єфрем Ярош'
            """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def students_in_groups():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT students.fullname
            FROM students
            JOIN groups ON students.group_id = groups.id
            WHERE groups.name = 'ПМ-22-1'
            """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def marks_for_students():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT marks.mark
            From marks
            JOIN students ON marks.student_id = students.id
            JOIN groups ON students.group_id = groups.id
            JOIN subjects ON marks.subject_id = subjects.id
            WHERE subjects.subject_name = 'Теорія імовірності'
            AND groups.name = 'ПМ-22-2'
            """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def teacher_avg_mark():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT subjects.subject_name, AVG(marks.mark) AS avg_grade
            FROM marks
            JOIN subjects ON marks.subject_id = subjects.id
            JOIN teachers ON subjects.teacher_id = teachers.id
            WHERE teachers.fullname = 'Єфрем Ярош'
            """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def students_attendance():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT subjects.subject_name
            FROM subjects
            JOIN marks ON marks.subject_id = subjects.id
            JOIN students ON marks.student_id = students.id
            WHERE students.fullname = 'Пилип Андрієнко'
            """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students

def teachers_and_students():
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        query = """
            SELECT subjects.subject_name
            FROM subjects
            JOIN teachers ON subjects.teacher_id = teachers.id
            JOIN marks ON marks.subject_id = subjects.id
            JOIN students ON marks.student_id = students.id
            WHERE students.fullname = 'Пилип Андрієнко' AND teachers.fullname = 'Єфрем Ярош'
            """
        cur.execute(query)
        top_students = cur.fetchall()
        return top_students
if __name__ == '__main__':
    top_student = teachers_and_students()
    print(top_student)



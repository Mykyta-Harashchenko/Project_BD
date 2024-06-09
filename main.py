from datetime import datetime, timedelta
import faker
from random import randint, choice
import sqlite3
import random

fake_students = 50
fake_groups = 3
fake_teachers = 4
fake_marks = 20

def generate_fake_data(fake_students, fake_teachers, fake_marks):
    students  = []
    groups = ['DB113', 'MA354', 'FM198']
    subjects = ['algebra', 'analytics', 'finance', 'PE', 'IT', 'biology' ]
    teachers = []
    marks = []
    fake_data = faker.Faker()

    for _ in range(fake_students):
        student = {'Name': fake_data.first_name(), 'Surname': fake_data.last_name()}
        students.append(student)
        print(student)

    for i in range(fake_teachers):
        teacher = {'Surname': fake_data.last_name(), 'Name': fake_data.first_name()}
        teachers.append(teacher)
        print(teacher)


    return students, teachers, groups, marks, subjects

def seed_grades():
    start_date = datetime.strptime('2022-09-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-05-31', '%Y-%m-%d')
    def get_list_dates(start_date: datetime, end_date: datetime):
        result = []
        current_date = start_date
        while current_date <= end_date:
            if current_date.isoweekday() < 6:
                result.append(current_date)
            current_date += timedelta(1)
        return result
    list_dates = get_list_dates(start_date, end_date)
def prepare_data(students, teachers, groups, marks, subjects)->tuple:
    for_students = []
    for student in students:
        for_students.append((student, ))

    for_groups = []
    for group in groups:
        for_groups.append((group, choice(students)))

    for_teachers = []

    for teacher in teachers:
        for_teachers.append((teacher, random.choice(groups)))

    for_subjects = []
    for subject in subjects:
        for_subjects.append(random.choice(subjects), )


    for_marks = []
    start_date = datetime.strptime('2022-09-01', '%Y-%m-%d')
    end_date = datetime.strptime('2023-05-31', '%Y-%m-%d')
    while start_date <= end_date:
        if start_date.isoweekday() < 6:
            for mark in marks:
                for_marks.append((choice(subjects), randint(1, 100)))
            start_date += timedelta(1)

    return for_marks, for_groups, for_subjects, for_teachers, for_students

def insert_data_to_db(students, teachers, groups, marks, subjects)->None:
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        sql_to_students = """INSERT INTO students(student_name, student_surname, group_id) VALUES (?)"""
        cur.executemany(sql_to_students, students)

        sql_to_groups = """INSERT INTO groups(group_name, student_id) VALUES (?, ?, ?)"""
        cur.executemany(sql_to_groups, groups)

        sql_to_teachers = """INSERT INTO teachers(teacher_name, teacher_surname, group_id) VALUES (?, ?, ?)"""
        cur.executemany(sql_to_teachers, teachers)

        sql_to_subjects = """INSERT INTO subjects(subject_name, teacher_id) VALUES (?, ?, ?)"""
        cur.executemany(sql_to_subjects, subjects)

        sql_to_marks = """INSERT INTO marks(subject_name, subject_mark, student_id) VALUES (?, ?, ?)"""
        cur.executemany(sql_to_marks, marks)


if __name__ == '__main__':
    students, teachers, groups, marks, subjects = prepare_data(*generate_fake_data(fake_students, fake_teachers, fake_marks))


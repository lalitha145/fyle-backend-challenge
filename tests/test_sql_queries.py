import sqlite3

def test_count_grade_A_assignments_by_teacher_with_max_grading():
    conn = sqlite3.connect('core/store.sqlite3')
    cursor = conn.cursor()
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', 'r') as file:
        sql = file.read()
    cursor.execute(sql)
    result = cursor.fetchall()
    assert len(result) > 0
    conn.close()

def test_number_of_graded_assignments_for_each_student():
    conn = sqlite3.connect('core/store.sqlite3')
    cursor = conn.cursor()
    with open('tests/SQL/number_of_graded_assignments_for_each_student.sql', 'r') as file:
        sql = file.read()
    cursor.execute(sql)
    result = cursor.fetchall()
    assert len(result) > 0
    conn.close()

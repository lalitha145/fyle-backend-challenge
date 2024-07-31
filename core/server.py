from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from core.models import Assignment, Teacher

@app.route('/principal/assignments', methods=['GET'])
def get_principal_assignments():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    assignments = Assignment.query.filter(Assignment.state.in_(['SUBMITTED', 'GRADED'])).all()
    return jsonify({"data": [assignment.to_dict() for assignment in assignments]})

@app.route('/principal/teachers', methods=['GET'])
def get_teachers():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    teachers = Teacher.query.all()
    return jsonify({"data": [teacher.to_dict() for teacher in teachers]})

@app.route('/principal/assignments/grade', methods=['POST'])
def grade_or_regrade_assignment():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    assignment = Assignment.query.get(data['id'])
    if assignment:
        assignment.grade = data['grade']
        assignment.state = 'GRADED'
        db.session.commit()
        return jsonify({"data": assignment.to_dict()})
    return jsonify({"error": "Assignment not found"}), 404

@app.route('/student/assignments', methods=['GET', 'POST'])
def student_assignments():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    if request.method == 'GET':
        student_id = request.headers.get('X-Student')
        assignments = Assignment.query.filter_by(student_id=student_id).all()
        return jsonify({"data": [assignment.to_dict() for assignment in assignments]})
    elif request.method == 'POST':
        data = request.json
        if 'id' in data:
            assignment = Assignment.query.get(data['id'])
            if assignment:
                assignment.content = data['content']
                assignment.updated_at = db.func.current_timestamp()
                db.session.commit()
                return jsonify({"data": assignment.to_dict()})
        else:
            new_assignment = Assignment(
                content=data['content'],
                state='DRAFT',
                student_id=request.headers.get('X-Student')
            )
            db.session.add(new_assignment)
            db.session.commit()
            return jsonify({"data": new_assignment.to_dict()})

@app.route('/student/assignments/submit', methods=['POST'])
def submit_assignment():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    assignment = Assignment.query.get(data['id'])
    if assignment:
        assignment.state = 'SUBMITTED'
        assignment.teacher_id = data['teacher_id']
        db.session.commit()
        return jsonify({"data": assignment.to_dict()})
    return jsonify({"error": "Assignment not found"}), 404

@app.route('/teacher/assignments', methods=['GET'])
def get_teacher_assignments():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    teacher_id = request.headers.get('X-Teacher')
    assignments = Assignment.query.filter_by(teacher_id=teacher_id).all()
    return jsonify({"data": [assignment.to_dict() for assignment in assignments]})

@app.route('/teacher/assignments/grade', methods=['POST'])
def grade_assignment():
    user_id = request.headers.get('X-Principal')
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json
    assignment = Assignment.query.get(data['id'])
    if assignment:
        assignment.grade = data['grade']
        assignment.state = 'GRADED'
        db.session.commit()
        return jsonify({"data": assignment.to_dict()})
    return jsonify({"error": "Assignment not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)

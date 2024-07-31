import pytest
from core.server import app, db
from core.models import Assignment, Teacher

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///store.sqlite3'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_get_principal_assignments(client):
    response = client.get('/principal/assignments', headers={'X-Principal': '5'})
    assert response.status_code == 200
    data = response.json['data']
    assert isinstance(data, list)

def test_get_teachers(client):
    response = client.get('/principal/teachers', headers={'X-Principal': '5'})
    assert response.status_code == 200
    data = response.json['data']
    assert isinstance(data, list)

def test_grade_or_regrade_assignment(client):
    # Assuming assignment with ID 1 exists
    response = client.post('/principal/assignments/grade', json={'id': 1, 'grade': 'A'}, headers={'X-Principal': '5'})
    assert response.status_code == 200
    data = response.json['data']
    assert data['grade'] == 'A'

def test_student_create_assignment(client):
    response = client.post('/student/assignments', json={'content': 'New Assignment'}, headers={'X-Principal': '2', 'X-Student': '2'})
    assert response.status_code == 200
    data = response.json['data']
    assert data['content'] == 'New Assignment'

def test_submit_assignment(client):
    # Assuming assignment with ID 1 exists and teacher with ID 2 exists
    response = client.post('/student/assignments/submit', json={'id': 1, 'teacher_id': 2}, headers={'X-Principal': '1', 'X-Student': '1'})
    assert response.status_code == 200
    data = response.json['data']
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

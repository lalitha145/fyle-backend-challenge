# Fyle Backend Challenge

## Setup

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd fyle_backend_challenge
    ```

2. **Setup virtual environment**
    ```bash
    virtualenv env --python=python3.8
    source env/bin/activate
    ```

3. **Install dependencies**
    ```bash
    pip install -r core/requirements.txt
    ```

4. **Run migrations**
    ```bash
    export FLASK_APP=core/server.py
    rm core/store.sqlite3
    flask db upgrade -d core/migrations/
    ```

5. **Start the server**
    ```bash
    bash run.sh
    ```

6. **Run tests**
    ```bash
    pytest -vvv -s tests/
    ```

## Docker

1. **Build and run Docker container**
    ```bash
    docker-compose build
    docker-compose up
    ```

## SQL Queries

- `count_grade_A_assignments_by_teacher_with_max_grading.sql`
- `number_of_graded_assignments_for_each_student.sql`

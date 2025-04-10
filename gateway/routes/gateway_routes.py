from flask import Blueprint, jsonify, render_template, request
import requests
from requests.exceptions import RequestException

gateway_bp = Blueprint('gateway_bp', __name__)

USER_URL = 'http://user:5002'
CONTROL_URL = 'http://controller:5001'
# USER_URL = 'http://localhost:5002'
# CONTROL_URL = 'http://localhost:5001'


@gateway_bp.route("/")
def login_page():
    return render_template("index.html")


# ===========================
# 👨‍🎓 STUDENT ENDPOINTS
# ===========================

@gateway_bp.route('/students/create', methods=['POST', 'GET'])
def create_students():
    if request.method == 'POST':
        # Get the form data
        name = request.form["name"]
        age = request.form["age"]
        course = request.form["course"]
        type = "student"
        username = request.form["username"]
        password = request.form["password"]

        student = {"name": name, "age": age, "course": course, "type": type, "username": username, "password": password}
        
        try:
            response = requests.post(f"{USER_URL}/students/create", json=student)
            if response.status_code == 200:
                json_response = response.json()
                return jsonify(json_response), 200
            else:
                return jsonify({"error": "Failed to create student", "details": response.text}), response.status_code
        except RequestException as e:
            return jsonify({"error": "User service unavailable", "details": str(e)}), 503
    
    return render_template("./user/create_student.html")
    

@gateway_bp.route('/students', methods=['GET'])
def get_students():
    try:
        response = requests.get(f"{USER_URL}/students")
        students = response.json()  # pega o JSON
        return render_template("./user/list_students.html", students=students)
    except RequestException as e:
        return jsonify({"error": "User service unavailable", "details": str(e)}), 503


@gateway_bp.route('/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_student(student_id):
    try:
        url = f"{USER_URL}/students/{student_id}"
        if request.method == 'GET':
            response = requests.get(url)
        elif request.method == 'PUT':
            response = requests.put(url, json=request.get_json())
        elif request.method == 'DELETE':
            response = requests.delete(url)
        return (response.text, response.status_code, response.headers.items())
    except RequestException as e:
        return jsonify({"error": "User service unavailable", "details": str(e)}), 503


# ===========================
# 👨‍🏫 TEACHER ENDPOINTS
# ===========================

@gateway_bp.route('/teachers/create', methods=['POST', 'GET'])
def create_teacher():
    if request.method == 'POST':
        # Get the form data
        name = request.form["name"]
        age = request.form["age"]
        type = "teacher"
        username = request.form["username"]
        password = request.form["password"]

        teacher = {"name": name, "age": age, "type": type, "username": username, "password": password}
        
        try:
            response = requests.post(f"{USER_URL}/teachers/create", json=teacher)
            if response.status_code == 200:
                json_response = response.json()
                return jsonify(json_response), 200
            else:
                return jsonify({"error": "Failed to create teacher", "details": response.text}), response.status_code
        except RequestException as e:
            return jsonify({"error": "User service unavailable", "details": str(e)}), 503
    
    return render_template("./user/create_teacher.html")

@gateway_bp.route('/teachers', methods=['GET'])
def get_teachers():
    try:
        response = requests.get(f"{USER_URL}/teachers")
        teachers = response.json()  # pega o JSON
        return render_template("./user/list_teachers.html", teachers=teachers)
    except RequestException as e:
        return jsonify({"error": "User service unavailable", "details": str(e)}), 503


@gateway_bp.route('/teachers/<int:teacher_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_teacher(teacher_id):
    try:
        url = f"{USER_URL}/teachers/{teacher_id}"
        if request.method == 'GET':
            response = requests.get(url)
        elif request.method == 'PUT':
            response = requests.put(url, json=request.get_json())
        elif request.method == 'DELETE':
            response = requests.delete(url)
        return (response.text, response.status_code, response.headers.items())
    except RequestException as e:
        return jsonify({"error": "User service unavailable", "details": str(e)}), 503


# ===========================
# 🧠 SESSION ENDPOINTS
# ===========================

@gateway_bp.route('/sessions/create', methods=['GET', "POST"])
def create():
    if request.method == 'POST':
        try:
            strategy = request.form.get('strategy')
            response = requests.post(f"{CONTROL_URL}/sessions/create", json={"strategy": strategy})
            if response.status_code == 200:
                sessions = response.json()  # pega o JSON
                return jsonify(sessions), 200
            else:
                return f"Erro ao buscar sessões: {response.status_code}", response.status_code
        except RequestException as e:
            return jsonify({"error": "Control service unavailable", "details": str(e)}), 503
    else:
        return render_template("./control/create_session.html")

@gateway_bp.route('/sessions', methods=['GET'])
def list_sessions():
    try:
        response = requests.get(f"{CONTROL_URL}/sessions")
        if response.status_code == 200:
            sessions = response.json()  # pega o JSON
            return render_template("./control/list_all_sessions.html", sessions=sessions)
        else:
            return f"Erro ao buscar sessões: {response.status_code}", response.status_code
    except RequestException as e:
        return jsonify({"error": "Control service unavailable", "details": str(e)}), 503


@gateway_bp.route('/sessions/status/<int:session_id>', methods=['GET'])
def get_session_status(session_id):
    try:
        response = requests.get(f"{CONTROL_URL}/sessions/status/{session_id}")
        return (response.text, response.status_code, response.headers.items())
    except RequestException as e:
        return jsonify({"error": "Control service unavailable", "details": str(e)}), 503


@gateway_bp.route('/sessions/start/<int:session_id>', methods=['POST'])
def start_session(session_id):
    try:
        response = requests.post(f"{CONTROL_URL}/sessions/start/{session_id}")
        return (response.text, response.status_code, response.headers.items())
    except RequestException as e:
        return jsonify({"error": "Control service unavailable", "details": str(e)}), 503


@gateway_bp.route('/sessions/end/<int:session_id>', methods=['POST'])
def end_session(session_id):
    try:
        response = requests.post(f"{CONTROL_URL}/sessions/end/{session_id}")
        return (response.text, response.status_code, response.headers.items())
    except RequestException as e:
        return jsonify({"error": "Control service unavailable", "details": str(e)}), 503

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import cv2
import face_recognition
from pyzbar import pyzbar
import os
import datetime
import json

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ams.db'
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(10))  

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course = db.Column(db.String(100))

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer)
    date = db.Column(db.String(50))
    status = db.Column(db.String(20))  
    method = db.Column(db.String(20))  


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(username=data['username'], password=hashed, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    if data['role'] == 'student':
        profile = StudentProfile(user_id=new_user.id, course=data.get('course', ''))
        db.session.add(profile)
        db.session.commit()
    return jsonify({'message': 'User registered'})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': access_token})
    return jsonify({'message': 'Invalid credentials'}), 401


def recognize_face(student_id):
    known_path = f"faces/{student_id}.jpg"
    if not os.path.exists(known_path):
        return False
    known_image = face_recognition.load_image_file(known_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]

    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        return False

    encodings = face_recognition.face_encodings(frame)
    if not encodings:
        return False

    result = face_recognition.compare_faces([known_encoding], encodings[0])
    return result[0]


def scan_qr_code():
    cam = cv2.VideoCapture(0)
    ret, frame = cam.read()
    cam.release()
    if not ret:
        return None
    decoded = pyzbar.decode(frame)
    return decoded[0].data.decode() if decoded else None


@app.route('/attendance/mark', methods=['POST'])
@jwt_required()
def mark_attendance():
    user = get_jwt_identity()
    if user['role'] != 'student':
        return jsonify({'message': 'Access denied'}), 403

    method = request.json.get('method')
    student_id = user['id']
    today = str(datetime.date.today())

    if method == 'face' and recognize_face(student_id):
        pass
    elif method == 'qr':
        code = scan_qr_code()
        if not code or code != f"student-{student_id}":
            return jsonify({'message': 'Invalid QR code'}), 401
    elif method == 'fingerprint':
        if not request.json.get('fingerprint_match'):
            return jsonify({'message': 'Fingerprint not matched'}), 401
    elif method == 'offline':
        records = request.json.get('offline_data', [])
        for rec in records:
            db.session.add(Attendance(
                student_id=student_id,
                date=rec['date'],
                status=rec['status'],
                method=rec['method']
            ))
        db.session.commit()
        return jsonify({'message': 'Offline data synced'})
    else:
        return jsonify({'message': 'Unsupported or failed method'}), 401

    new_att = Attendance(student_id=student_id, date=today, status='present', method=method)
    db.session.add(new_att)
    db.session.commit()
    return jsonify({'message': 'Attendance marked via ' + method})

@app.route('/student/stats', methods=['GET'])
@jwt_required()
def student_stats():
    user = get_jwt_identity()
    if user['role'] != 'student':
        return jsonify({'message': 'Access denied'}), 403
    student_id = user['id']
    records = Attendance.query.filter_by(student_id=student_id).all()
    stats = {}
    for rec in records:
        stats[rec.date] = rec.status
    return jsonify(stats)


@app.route('/teacher/attendance/<int:student_id>', methods=['GET'])
@jwt_required()
def view_attendance(student_id):
    user = get_jwt_identity()
    if user['role'] != 'teacher':
        return jsonify({'message': 'Access denied'}), 403

    records = Attendance.query.filter_by(student_id=student_id).all()
    return jsonify([{ 'date': r.date, 'status': r.status, 'method': r.method } for r in records])

@app.route('/teacher/students', methods=['GET'])
@jwt_required()
def list_students():
    user = get_jwt_identity()
    if user['role'] != 'teacher':
        return jsonify({'message': 'Access denied'}), 403
    students = StudentProfile.query.all()
    return jsonify([{'id': s.id, 'user_id': s.user_id, 'course': s.course} for s in students])

@app.route('/teacher/student', methods=['POST'])
@jwt_required()
def add_student():
    user = get_jwt_identity()
    if user['role'] != 'teacher':
        return jsonify({'message': 'Access denied'}), 403
    data = request.json
    new_user = User(username=data['username'], password=bcrypt.generate_password_hash(data['password']).decode('utf-8'), role='student')
    db.session.add(new_user)
    db.session.commit()
    profile = StudentProfile(user_id=new_user.id, course=data['course'])
    db.session.add(profile)
    db.session.commit()
    return jsonify({'message': 'Student added'})

@app.route('/backup', methods=['GET'])
@jwt_required()
def backup_data():
    user = get_jwt_identity()
    if user['role'] != 'teacher':
        return jsonify({'message': 'Access denied'}), 403
    data = [
        {'student_id': a.student_id, 'date': a.date, 'status': a.status, 'method': a.method}
        for a in Attendance.query.all()
    ]
    with open('backup.json', 'w') as f:
        json.dump(data, f)
    return jsonify({'message': 'Backup complete'})


if __name__ == '__main__':
    if not os.path.exists('ams.db'):
        db.create_all()
    app.run(debug=True)

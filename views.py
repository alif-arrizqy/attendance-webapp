from flask import Flask, Blueprint, render_template, Response, request, redirect, url_for, flash
import cv2
import datetime, time
import os, sys
import numpy as np
import face_recognition
from controllers import *

global capture, npm_mahasiswa, nama_lengkap
capture = 0

views = Blueprint("views", __name__)

# redis connection
red = redis.StrictRedis(
    host="localhost",
    password="",
    port=6379,
    db=0
)

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it
print('load model')
load_model()

def detect_face(frame):
    # decode the face encoding and name
    # retrieve the serialized data from Redis
    serialized_known_face_encodings = red.lrange('known_face_encodings', 0, -1)
    serialized_known_face_names = red.lrange('known_face_names', 0, -1)

    # Deserialize the data
    known_face_encodings = [pickle.loads(face_encoding) for face_encoding in serialized_known_face_encodings]
    known_face_names = [pickle.loads(face_name) for face_name in serialized_known_face_names]

    # Resize frame of video to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert BGR to RGB
    # rgb_small_frame = small_frame[:, :, ::-1] # windows
    rgb_small_frame = np.ascontiguousarray(small_frame[:, :, ::-1]) # linux

    # Find all the faces and face encodings
    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Compare faces with known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        npm = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            npm = known_face_names[first_match_index]

        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # widen the box
        cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), (0, 0, 255), 2)

        # Draw a label with a npm below the face
        cv2.rectangle(frame, (left - 12, bottom - 10), (right + 12, bottom + 15), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, npm, (left, bottom + 12), font, 1.0, (255, 255, 255), 1)
    return frame

# generate frame by frame from camera
def gen_frames():
    global capture
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame= detect_face(frame)
        if capture:
            capture = 0
            now = datetime.datetime.now()
            p = os.path.sep.join(['shots', f"shot_{now.strftime('%Y%m%dT%H%M%S')}.jpg"])
            cv2.imwrite(p, frame)
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass
        else:
            pass

@views.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@views.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
        return render_template('home.html')
    elif request.method=='GET':
        return render_template('home.html')
    return render_template('home.html')

# register section
@views.route('/video_feed_register')
def video_feed_register():
    return Response(gen_frames_registrasi(), mimetype='multipart/x-mixed-replace; boundary=frame')

def detect_face_register(frame):
    return frame

# generate frame by frame from camera
def gen_frames_registrasi():
    global capture
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame = detect_face_register(frame)

        if capture:
            capture = 0
            # now = datetime.datetime.now()
            # p = os.path.sep.join(['register_user', f"image_{npm_mahasiswa}_{now.strftime('%Y%m%dT%H%M%S')}.jpg"])
            p = os.path.sep.join(['register_user', f"image_{npm_mahasiswa}.jpg"])
            cv2.imwrite(p, frame)

            # insert data to database
            register_users(npm_mahasiswa, nama_lengkap, f"image_{npm_mahasiswa}.jpg")
        try:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        except Exception as e:
            pass
        else:
            pass

@views.route("/registrasi", methods=['GET', 'POST'])
def registrasi():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture, npm_mahasiswa, nama_lengkap
            # check npm
            if check_npm(request.form.get('npm')):
                flash("Gagal! NPM sudah terdaftar", category="danger")
                return redirect(url_for('views.registrasi'))
            else:
                capture = 1
                npm_mahasiswa = request.form.get('npm')
                nama_lengkap = request.form.get('nama_lengkap')
                flash("Pendaftaran Berhasil! Silahkan Melakukan Absen", category="success")

        return redirect(url_for('views.registrasi'))
    elif request.method=='GET':
        return render_template('registrasi.html')

@views.route("/")
def index():
    return render_template("home.html")

@views.route("/daftar-hadir")
def daftar_kehadiran():
    return render_template("daftar_hadir.html")


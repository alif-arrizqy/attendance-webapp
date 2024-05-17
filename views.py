from flask import Flask, Blueprint, render_template, Response, request, redirect, url_for
import cv2
import datetime, time
import os, sys
import numpy as np
import face_recognition
views = Blueprint("views", __name__)


global capture, npm_mahasiswa
capture=0

#make shots directory to save pics
try:
    os.mkdir('./shots')
except OSError as error:
    pass

#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

camera = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
alif_image = face_recognition.load_image_file("biden.jpg")
alif_face_encoding = face_recognition.face_encodings(alif_image)[0]

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    alif_face_encoding,
    obama_face_encoding
]
known_face_names = [
    "ALIF AA",
    "obama"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def detect_face(frame):
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
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Scale back up face locations
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        # cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        # widen the box
        cv2.rectangle(frame, (left - 20, top - 20), (right + 20, bottom + 20), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left - 12, bottom - 10), (right + 12, bottom + 15), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 10, bottom + 12), font, 1.0, (255, 255, 255), 1)
    return frame

# generate frame by frame from camera
def gen_frames():
    global capture, npm_mahasiswa
    while True:
        success, frame = camera.read()
        if not success:
            break
        frame= detect_face(frame) 
        if capture:
            print(npm_mahasiswa)
            capture = 0
            now = datetime.datetime.now()
            p = os.path.sep.join(['shots', "shot_{}.jpg".format(str(now).replace(":",''))])
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
    return Response(gen_frames_registrasi(register=True), mimetype='multipart/x-mixed-replace; boundary=frame')

def detect_face_register(frame):
    return frame

# generate frame by frame from camera
def gen_frames_registrasi(register=False):
    global capture
    while True:
        success, frame = camera.read()
        if not success:
            break
        if register:
            frame = detect_face_register(frame)
        else:
            frame= detect_face(frame) 
        if capture:
            capture = 0
            now = datetime.datetime.now()
            p = os.path.sep.join(['register_user', f"image_{npm_mahasiswa}_{str(now).replace(':','')}.jpg"])
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

@views.route("/registrasi", methods=['GET', 'POST'])
def registrasi():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture, npm_mahasiswa
            capture = 1
            npm_mahasiswa = request.form.get('npm')
        # return render_template('home.html')
        return redirect(url_for('views.registrasi'))
    elif request.method=='GET':
        return render_template('registrasi.html')

@views.route("/")
def index():
    return render_template("home.html")

@views.route("/daftar-hadir")
def daftar_kehadiran():
    return render_template("daftar_hadir.html")


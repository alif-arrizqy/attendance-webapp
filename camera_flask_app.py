from flask import Flask, render_template, Response, request
import cv2
import datetime, time
import os, sys
import numpy as np
import face_recognition

global capture
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
alif_image = face_recognition.load_image_file("alif.jpg")
alif_face_encoding = face_recognition.face_encodings(alif_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    alif_face_encoding,
]
known_face_names = [
    "ALIF AA"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True


def detect_face(frame):
    # Resize frame of video to 1/4 size for faster processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:, :, ::-1]  # Convert BGR to RGB

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
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


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


@app.route('/')
def index():
    return render_template('index.html')
    
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera
    if request.method == 'POST':
        if request.form.get('click') == 'Capture':
            global capture
            capture=1
    elif request.method=='GET':
        return render_template('index.html')
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
    
camera.release()
cv2.destroyAllWindows()     
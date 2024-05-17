import cv2
import face_recognition
import numpy as np
import os
from database import connection

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
    # "ALIF AA",
    "biden",
    "obama"
]
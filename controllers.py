import face_recognition
import numpy as np
import os
import pickle
from database.connection import *
from dotenv import load_dotenv
import redis

load_dotenv()

# Use a connection pool for Redis
pool = redis.ConnectionPool(
    host="localhost",
    password="",
    port=6379,
    db=0
)

# Create the directory if it doesn't exist
os.makedirs('./register_user', exist_ok=True)

def load_model():
    # Create a new Redis connection
    red = redis.Redis(connection_pool=pool)

    # Create a new database connection
    db = Database(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"))

    # get data from database
    data = db.select(table_name="users")
    
    # filter data, get npm, nama_lengkap, foto
    npm = [d[1] for d in data]
    nama_lengkap = [d[2] for d in data]
    foto = [d[3] for d in data]

    # Load a sample picture and learn how to recognize it.
    known_face_encodings = []
    known_face_names = []
    for i in range(len(data)):
        image = face_recognition.load_image_file(f"./register_user/{foto[i]}")
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(npm[i])

    # cache the data face encoding and name
    # Serialize the data
    try:
        serialized_known_face_encodings = [pickle.dumps(face_encoding) for face_encoding in known_face_encodings]
        serialized_known_face_names = [pickle.dumps(face_name) for face_name in known_face_names]
    except Exception as e:
        serialized_known_face_encodings = []
        serialized_known_face_names = []

    # Store the serialized data in Redis
    for face_encoding in serialized_known_face_encodings:
        red.lpush('known_face_encodings', face_encoding)

    for face_name in serialized_known_face_names:
        red.lpush('known_face_names', face_name)

    return known_face_encodings, known_face_names

def check_npm(npm):
    # Create a new database connection
    db = Database(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"))

    is_exist = db.find(table_name="users", columns="npm", condition=f"npm='{npm}'")
    if is_exist:
        return True
    else:
        return False

def register_users(npm, nama_lengkap, foto):
    # Create a new database connection
    db = Database(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"))

    db.insert(table_name="users", columns="npm, nama_lengkap, foto", values=(npm, nama_lengkap, foto))
    load_model()
    return True

def attendance(npm, tanggal_absen, foto):
    # Create a new database connection
    db = Database(os.getenv("DB_NAME"), os.getenv("DB_USER"), os.getenv("DB_PASSWORD"), os.getenv("DB_HOST"), os.getenv("DB_PORT"))

    db.insert(table_name="attendance", columns="npm, tanggal_absen, foto", values=(npm, tanggal_absen, foto))
    return True
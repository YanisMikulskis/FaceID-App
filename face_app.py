import sqlite3
import sqlalchemy.exc
from imutils import paths
import face_recognition
import pickle
import cv2
import os
import re
from face_db import *
from datetime import date
import numpy

imagePaths: list = list(paths.list_images('Images'))
data_faces: dict = dict()
for people_photo in imagePaths:
    name: str = re.findall(r'([^/\\]+)\.(jpg|jpeg|png|gif|bmp|HEIC)$', people_photo)[0][0]
    image: numpy.ndarray = cv2.imread(people_photo)
    rgb: numpy.ndarray = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes: list = face_recognition.face_locations(rgb, model='hog')
    encode_face: list = face_recognition.face_encodings(rgb, boxes)
    data_faces.setdefault(name, encode_face)

for name, face in data_faces.items():
    people: Faces = Faces(
        name=name,
        birthday=date(1995, 7, 30),
        code_face=pickle.dumps(face)
    )
    db_session.add_all([people])
    try:
        db_session.commit()
    except sqlalchemy.exc.IntegrityError:
        print(f'Такое лицо уже существует в базе!')
    else:
        print(f'Новое лицо добавлено! И это {name}')
    db_session.rollback()

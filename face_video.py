import face_recognition
import pickle
import cv2
import numpy

from face_db import *
from typing import Callable, Union

cascPathface: str = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade: cv2.CascadeClassifier = cv2.CascadeClassifier(cascPathface)
video_capture: cv2.VideoCapture = cv2.VideoCapture(0)
while cv2.waitKey(1) < 0:
    ret, frame = video_capture.read()
    fps: float = video_capture.get(cv2.CAP_PROP_FPS)

    gray: numpy.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces: tuple = faceCascade.detectMultiScale(gray,
                                                scaleFactor=1.1,
                                                minNeighbors=5,
                                                minSize=(60, 60),
                                                flags=cv2.CASCADE_SCALE_IMAGE)
    rgb: numpy.ndarray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame: numpy.ndarray = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)

    encoding_camera: list = face_recognition.face_encodings(small_frame)

    numpy_faces: list = list(map(lambda code: code[0], db_session.query(Faces.code_face).all()))
    numpy_faces: list = list(map(lambda code: pickle.loads(code), numpy_faces))

    names_on_frames: list = []
    if encoding_camera:
        for en in encoding_camera:
            def matches_recursion(emb: list) -> Union[Callable, str]:
                """
                Рекурсивная функция проверки человека, который смотрит в камеру.
                Сравниваем эмбдендинг лица, которое видит камера с эмбдендингом в базе данных (через compare_faces)
                """
                if not emb:
                    names_on_frames.append('Noname human')
                    return f'В камеру смотрит неизвестный человек!'
                matches: list = face_recognition.compare_faces(emb[0], en)

                if matches[0]:
                    name_viewer: str = (db_session.query(Faces).
                                        filter(Faces.code_face == pickle.dumps(emb[0])).first().name)
                    names_on_frames.append(name_viewer)

                    return f'{name_viewer} смотрит в камеру'
                if not matches[0]:
                    return matches_recursion(emb[1:])


            matches_recursion(emb=numpy_faces)
            for ([x, y, w, h], name) in zip(faces, names_on_frames):
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, name, (x, h), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    else:
        print(f'В камеру никто не смотрит! :(')
    cv2.imshow('NeuroFace', frame)
video_capture.release()
cv2.destroyAllWindows()

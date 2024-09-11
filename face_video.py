import concurrent.futures

import face_recognition
import imutils
import pickle
import time
import cv2
import os
from face_db import *
from typing import Callable, Union

# находим в библиотеке cv2 файл aarcascade_frontalface_alt2.xml с каскадами Хаара
cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
# cascPathLBP = os.path.dirname(cv2.__file__) + "/data/lbpcascade_frontalface.xml"

# загружаем найденный файлик в каскадный классификатор
faceCascade = cv2.CascadeClassifier(cascPathface)
# faceCascade = cv2.CascadeClassifier(cascPathLBP)
# сохраняем в переменную лица в файле pickle открывая его на чтение
# with open('face_enc', 'rb') as face_pickley:
#     data = pickle.loads(face_pickley.read())

# переменная захватывающая видеопоток (подключаемся к вебке)
video_capture = cv2.VideoCapture(0)
# цикл видеопоток


while cv2.waitKey(1) < 0:
    # захватываем кдары из видеопотока
    # ловим кадр в цикле. ret - параметр, которые имеет булево значение. True, если все ок. frame - сам кадр в видео массива numpy
    ret, frame = video_capture.read()

    fps = video_capture.get(cv2.CAP_PROP_FPS)
    print(f'Current fps {fps}')

    # ----

    # делаем кадр из BGR серым (классификатор может работать только с оттенками серого)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # faces - это список с параметрами всех обнаруженных лиц на сером кадре
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)  # для HAAR
    # faces = faceCascade.detectMultiScale(gray,
    #                                      scaleFactor=1.1,
    #                                      minNeighbors=5) #для LBP

    # делаем кадр из BGR цветным (RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # создаем эмбдендинги лиц на цветном изображении
    # encoding_camera = encode(rgb)
    small_frame = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)  # уменьшаем размер кадра иначе томрозит, но для пет проекта вполне достаточно
    encoding_camera = face_recognition.face_encodings(small_frame)

    #
    # names = []

    # print(f'encoding camera {encoding_camera}')

    # all_names_DB = [name[0] for name in db_session.query(Faces.name).all()]

    # преобразуем из формата pickle в numpy все эмбендинги из БД и сохраним в отдельную переменную
    # для начала извлечем из БД все эмбендинги и создадим из них список( извлекаются они кортежами и от них нужно

    # ---------
    # нужно избавиться, поэтому через лямбду извлекаем нулевой(и единственный) элемент кортежа)
    numpy_faces = list(map(lambda x: x[0], db_session.query(Faces.code_face).all()))
    # # и теперь через лямбду "распикливаем" эмбендинги
    numpy_faces = list(map(lambda x: pickle.loads(x), numpy_faces))
    names_on_frames = []

    # без лиц в кадре этот цикл не запустится!
    # #---------
    if encoding_camera:
        for en in encoding_camera:
            def matches_recursion(emb: list) -> Union[Callable, str]:
                """
                Рекурсивная функция проверки человека, который смотрит в камеру. Сравниваем эмбдендинг лица,
                которое видит камера с эмбдендингом в базе данных (через compare_faces)
                """
                if not emb:
                    names_on_frames.append('Noname human')
                    return f'В камеру смотрит неизвестный человек!'
                matches = face_recognition.compare_faces(emb[0], en)
                # Если в камеру смотрит кто-то, чей эмбендинг лица близок к одному из эмбдендингов в базе. matches
                # имеет вид списка с булевым значением ([True] или [False])
                if matches[0]:
                    # для сравнивания в запросе к БД прогоняем опять через пикли
                    # (в БД эмбендинги хранятся в пикли формате)
                    name_viewer = db_session.query(Faces).filter(Faces.code_face == pickle.dumps(emb[0])).first().name
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
    # -----
    cv2.imshow('NeuroFace', frame)
    # if cv2.waitKey(0):
    #     break
video_capture.release()  # закрытие видео
cv2.destroyAllWindows()  # закрытие всех созданных окон

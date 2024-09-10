import face_recognition
import imutils
import pickle
import time
import cv2
import os
from face_db import *
#находим в библиотеке cv2 файл aarcascade_frontalface_alt2.xml с каскадами Хаара
cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
#загружаем найденный файлик в каскадный классификатор
faceCascade = cv2.CascadeClassifier(cascPathface)
#сохраняем в переменную лица в файле pickle открывая его на чтение
with open('face_enc', 'rb') as face_pickley:
    data = pickle.loads(face_pickley.read())
print(data['Vika'])
print(f'stream start')
#переменная захватывающая видеопоток (подключаемся к вебке)
video_capture = cv2.VideoCapture(0)
#цикл видеопоток
var = 0
# w
while var < 10:
    #захватываем кдары из видеопотока
    #ловим кадр в цикле. ret - параметр, которые имеет булево значение. True, если все ок. frame - сам кадр в видео массива numpy
    ret, frame = video_capture.read()


    #делаем кадр из BGR серым (классификатор может работать только с оттенками серого)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #faces - это список с параметрами всех обнаруженных лиц на сером кадре
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60,60),
                                         flags=cv2.CASCADE_SCALE_IMAGE)
    #делаем кадр из BGR цветным (RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # создаем эмбдендинги лиц на цветном изображении
    encoding_camera = face_recognition.face_encodings(rgb)

    names = []
    # print(f'encoding camera {encoding_camera}')

    # all_names_DB = [name[0] for name in db_session.query(Faces.name).all()]
    #
    # yanis_encode = db_session.query(Faces).filter(Faces.name=='Yanis').first().code_face
    #
    # print(f'Yannis {type(yanis_encode)}')
    # yanis_loads = pickle.loads(yanis_encode)
    # print(f'Yanis numpy {type(yanis_loads)}')
    # print(f'all_nameeeee {all_names_DB}')
    # преобразуем из формата pickle в numpy все эмбендинги из БД и сохраним в отдельную переменную
    # для начала извлечем из БД все эмбендинги и создадим из них список( извлекаются они кортежами и от них нужно
    # нужно избавиться, поэтому через лямбду извлекаем нулевой(и единственный) элемент кортежа)
    numpy_faces = list(map(lambda x: x[0], db_session.query(Faces.code_face).all()))
    # и теперь через лямбду "распикливаем" эмбендинги
    numpy_faces = list(map(lambda x: pickle.loads(x), numpy_faces))

    print(f'embeds {numpy_faces}')
    # без лиц в кадре этот цикл не запустится!
    if encoding_camera:
        for en in encoding_camera:
            def matches_recursion(emb):
                if not emb:
                    print(f'В камеру смотрит неизвестный человек!')
                    return
                matches = face_recognition.compare_faces(emb[0], en)

                if matches[0]:
                    print(emb[0])
                    # для сравнивания в запросе к БД прогоняем опять через пикли (в БД эмбендинги хранятся в пикли формате
                    name_viewer = db_session.query(Faces).filter(Faces.code_face==pickle.dumps(emb[0])).first().name
                    print(f'{name_viewer} смотрит в камеру')
                    return
                elif not matches[0]:
                    return matches_recursion(emb[1:])
            matches_recursion(emb=numpy_faces)
    else:
        print(f'В камеру никто не смотрит! :(')





        # face_name = db_session.query(Faces).filter(Faces.name == 'Yanis').first().code_face
        # print(f'face_name {face_name}')
        # a_pickle = pickle.loads(face_name)
        # matches = face_recognition.compare_faces(a_pickle, en)
        # print(f'matches {matches}')
        # if matches[0]:
        #     print(f'Yanis смотрит в камеру')
        # elif not matches[0]:
        #     print(f'не смотрит')

    # for name in all_names_DB:
    #     face_name = db_session.query(Faces).filter(Faces.name==name).first().code_face
    #     print(f'face_name {type(face_name)}')
    #
    #
    #     a_pickle = pickle.loads(face_name)
    #     print(f'a picl {a_pickle}')
    #     print(f'encodingssss {encoding_camera}')
    #     matches = face_recognition.compare_faces(encoding_camera, a_pickle)
    #     if matches:
    #         name_cat = db_session.query(Faces).filter(Faces.code_face==encoding_DB).first().name
    #         print(f'Сейчас в камеру смотрит {name_cat}')
    #     else:
    #         print(f'Никто не смотрит')


    # for encoding in encodings:
    #     code_in_db =
    #     matches = face_recognition.compare_faces()
    #     face_in_camera = db_session.query(Faces).filter(Faces.code_face==encoding).first().name
    #     print(face_in_camera)
    #     matches = face_recognition.compare_faces()
    # запускаем цикл по эмбендингам на кадрах вебкамеры. Ищем софпадение с эмбеднингом лица, сохраненным в БД
    # (пока в отдельном пикли файле).При совпадении - возвращаем True
    # for encoding in encodings:
    #     matches = face_recognition.compare_faces(data["Yanis"], encoding)
    #     print(data['Yanis'])
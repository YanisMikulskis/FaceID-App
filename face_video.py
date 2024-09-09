import face_recognition
import imutils
import pickle
import time
import cv2
import os
#находим в библиотеке cv2 файл aarcascade_frontalface_alt2.xml с каскадами Хаара
cascPathface = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
#загружаем найденный файлик в каскадный классификатор
faceCascade = cv2.CascadeClassifier(cascPathface)
#сохраняем в переменную лица в файле pickle открывая его на чтение
with open('face_enc', 'rb') as face_pickley:
    data = pickle.loads(face_pickley.read())
print(data)
print(f'stream start')
#переменная захватывающая видеопоток (подключаемся к вебке)
video_capture = cv2.VideoCapture(0)
#цикл видеопоток
var = 0
# w
while var < 10:
    #захватываем кдары из видеопотока
    print(video_capture)
    #ловим кадр в цикле. ret - параметр, которые имеет булево значение. True, если все ок. frame - сам кадр в видео массива numpy
    ret, frame = video_capture.read()

    var += 1
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
    encodings = face_recognition.face_encodings(rgb)
    names = []
    # запускаем цикл по эмбендингам на кадрах вебкамеры. Ищем софпадение с эмбеднингом лица, сохраненным в БД
    # (пока в отдельном пикли файле).При совпадении - возвращаем True
    for encoding in encodings:
        matches = face_recognition.compare_faces(data["Yanis"], encoding)
        # print(matches)
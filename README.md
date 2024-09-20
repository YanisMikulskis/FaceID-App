## FaceID-App
 Smart face verification app
 
 Приложение для распознавания лиц. Для корректной работы требуется вебкамера.

## Стек
- Python > 3.11
- opencv-python == 4.19.0.84
- SQL Alchemy
- sqlite3
- face_recognition
- imutils
- PyCharm Professional
- macOS Sequoia ver.15.0
- Git

## Лицензия

MIT

# Общее описание работы кода (инструкция)
## Содержание проекта:
Данный проект содержит 3 .py модуля (2 основных, 1 дополнительный)

face_db.py


    Модуль для работы с базой данных лиц и их цифровых копий (эмбендингов):
    connect - подключаемся (или создаем) базу данных
    engine - создем движок 
    metadata - переменная для создания таблиц
    Base - базовый класс (будем от него наследоваться при создании таблиц)
    Faces - таблица лиц. состоит из 4 столбцов: id, имени, даты рождения, 
    эмбендинга(цифровой копии лица, созданной нейросетью)
    Создаем таблицу и сессию работы с БД

face_app.py


    Приложение для добавления лиц в БД. Чтобы добавить лицо в БД, для начала необходимо загрузить
    папку с фотографией этого лица в папку Images. Лицо должно быть четка видно. Чем четче - тем точнее 
    эмбендинг. Дальше запускаем код.
    imagePaths - пути к фотографиям в виде списка. Обращаемся к папке Images.
    data_faces - пустой словарь для пар имя: эмбендинг лица.
    Запускаем цикл по списку путей к фотографиям. Каждое фото называется именем человека, изображенного на фото.
    Обязательно нужно называть фотографии именно так, чтобы имена корректно подгружались в БД.
    name - имя фотографии, т.е. человека на фото. С помощью регулярки извлекаем имя и сохраняем в переменную
    image - прочитываем изображение с помощью cv2 (OpenCV-python) и сохраняем результат в переменную.
    rgb - конвертируем получившееся изображение в dlib (RGB) и сохраняем в переменную
    boxes - находим лица на dlib-изображении и сохраняем в переменную
    encode_faces - создаем эмбендинги лиц в найденном лице на изображении
    Добавляем получившееся имя и эмбендинг в словарь
    Проделываем тоже самое со всеми лицами и заполняем словарь data_faces

    Запускаем цикл по получившемуся словарю.
    Создаем объект для БД
    Добавляем объект в БД
    Отлавливаем ошибку ситуации, когда лицо уже такое есть.
    Если все ок - коммитим и выводим сообщение об успешном добавлении. Иначе - выводим сообщение о том, что
    такое лицо уже есть.

    
face_video.py


    Приложение для подключения к вебкамере и нахождению лица.
    Импортируем все нужное.
    cascPathface - путь к каскаду. Состоит из пути к директории с cv2 и выбранному каскаду. Используем каскады Хаара.
    faceCascade - загружаем найденный каскад в каскадный классификатор
    video_capture - переменная, захватывающая видеопоток (подключаемся к вебке)
    Запускаем цикл видеопотока до тех пор, пока не будет нажата любая кнопка, чтобы вебку отключить.
    ret, frame - переменные успешного включения вебки(bool type) и кадр(массив numpy) соответственно.
    fps - количество кадров в секунду (для информации)

    Делаем кадр из BGR серым (классификатор может работать только с оттенками серого)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces - это список с параметрами всех обнаруженных лиц на сером кадре
    faces = faceCascade.detectMultiScale(gray,
                                         scaleFactor=1.1,
                                         minNeighbors=5,
                                         minSize=(60, 60),
                                         flags=cv2.CASCADE_SCALE_IMAGE) - это настройка для каскада HAAR
 
   
    делаем кадр из BGR цветным (RGB)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    Уменьшаем размер кадра (иначе тормозит), но для пет проекта вполне достаточно  

    small_frame = cv2.resize(rgb, (0, 0), fx=0.25, fy=0.25)
    encoding_camera = face_recognition.face_encodings(small_frame) - список лиц в кадре камеры (может быть пустым,
    если лиц нет)  

    Далее нам нужно преобразовать обратно из формата pickley в numpy эмбендинги лиц и сохранить в 
    отдельную переменную. Будем это делать для сравнения лиц в БД и в кадре (в кадре они считываются в numpy)
    Для начала извлечем из БД все эмбендинги и создадим из них список (извлекаются они кортежами и от них 
    нужно нужно избавиться, поэтому через лямбду извлекаем нулевой(и единственный) элемент кортежа). 
    А затем "распикливаем" эмбендинги.
    numpy_faces - итоговый список. 
    names_on_frames - подготовим заранее список для имен лиц.
    if encoding_camera: если камера обнаружила лицо.

    Запускаем рекурсивную функцию проверки совпадений лиц из списка numpy_faces.
    Базовый случай: если совпадений не найдено, значит в камеру смотрит неизвестный человек.
    Совпадения проверяем через face_recongnition.compare_faces - сравниваем поочередно каждый первый
    элемент на каждом ходе рекурси (постепенно срезая список к концу) с лицом на камере (если оно найдено!).
    Делаем такую проверку на каждой итерации цикла по списку обнаруженных лиц.
    Если совпадение найдено:
    name_viewer - находим в бд поле, имеющее совпадающее лицо, которое у нас на текущей итерации рекурсии. 
    Лицо прогоняем через пикли, так как в БД они хранятся именно в таком формате. Извлекаем имя из этого поля.
    И добавляем его в список.
    
    Шаг рекурсии: если лицо не находим, то проверяем следующее лицо в списке лиц БД.


    После вызова рекурсии и окончания ее работы, запускаем цикл по "склееным" спискам обнаруженных на кадре лиц
    с именами. 
    cv2.rectangle - обводка вокруг лиц
    cv2.putText - текст с именем в обводке
    Если лиц в кадре не найдено, то выводится сообщение, что в камеру никто не смотрит.

    cv2.imshow - показ окна и кадра в нем.
    video_capture.release() - закрытие видео
    cv2.destroyAllWindows() - закрытие всех созданных окон

Чтобы закрыть окно видеопотока, нужно нажать любую клавишу на клавиатуре.

# import cv2
# import argparse
# import os
# parser = argparse.ArgumentParser(description='Videos for images')
# # parser.add_argument('indir', type=str, help='Input dir for videos')
# # parser.add_argument('outdir', type=str, help='Output dir for image')
# parser.add_argument('--my_optional', type=int, default=2, help='provide an integer(default:2)')
# parser.add_argument('--test_optional', type=int, default=10, help='provide an integer(default:2)')
# args = vars(parser.parse_args())
# print(args)
import sqlite3

import sqlalchemy.exc
# import sqlalchemy.exc
#
# ap = argparse.ArgumentParser()
#
# # ap.add_argument('-d', '--dir', required=1)
#
# ap.add_argument('-i', '--image', required=True, help='path to input image')
#
# args = vars(ap.parse_args())
# print(os.getcwd())
# # image = cv2.imread(args['Images/', 'image'], cv2.IMREAD_GRAYSCALE)
# # image_horses = cv2.imread(args['Images/HewHorses.png'], cv2.IMREAD_GRAYSCALE)
# # image_horses_new = cv2.imread('Images/Horses.jpeg', cv2.IMREAD_GRAYSCALE)
# image_args = cv2.imread(args['image'], cv2.IMREAD_GRAYSCALE)
#
# cv2.imshow('Horses_window', image_args)
# cv2.waitKey(0)
# h = image.shape[0]
# w = image.shape[1]
# print(f'w: {w}')
# print(f'h: {h}')
# print(os.getcwd())
# print(image)
# # cv2.imwrite('Images/HewHorses.png', image)

from imutils import paths
import face_recognition
import pickle
import cv2
import os
import re
from face_db import *
from datetime import date

imagePaths = list(paths.list_images('Images'))
data_faces = dict()
for people_photo in imagePaths:
    name = re.findall(r'([^/\\]+)\.(jpg|jpeg|png|gif|bmp|HEIC)$', people_photo)[0][0]
    image = cv2.imread(people_photo)  # загружаем изображение с помощью cv2
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # конвертация в dlib (RGB)
    boxes = face_recognition.face_locations(rgb, model='hog')  # находим лица на изображении в dlib формате изображения
    encode_face = face_recognition.face_encodings(rgb, boxes)  # создаем эмбендинги лиц в найденном лице на изображении

    data_faces.setdefault(name, encode_face)

for name, face in data_faces.items():
    people = Faces(
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

    # finally:
    #     db_session.close()
print(db_session.query(Faces).all())

#
# test_book = Library_Flask(title='title test',
#                           author='title author',
#                           year='title year',
#                           is_checked_out=1,
#                           personal_number = last_number + 1,
#                           user_book_id = None) # создаем книгу
# # db_session.add_all([test_book]) # добавляем в бд
# # db_session.commit()# коммитим


# with open('face_enc', 'wb') as faces_file:
#     faces_file.write(pickle.dumps(data_faces))


# Информация для sqlalchemy

# book = ['Влюбленные в книги не спят в одиночестве', 'Современная зарубежная литература', '2015']
# title_book = book[0]
# author_book = book[1]
# year = book[2]
#
#
# new_book = Library_Flask(title=title_book,
#                          author=author_book,
#                          year=year,
#                          is_checked_out=1,
#                          personal_number=1000,
#                          user_book_id=None)
#
# db_session.add_all([new_book])

# for user in range(2):
# new_user = User_Flask(
#     name=faker_.first_name_male(),
#     email=faker_.ascii_free_email()
# )
#
# db_session.add_all([new_user])
# db_session.commit()


# #вывести название книги по id в условии (может варьироваться)
# book_test = db_session.query(Library_Flask).filter(Library_Flask.id==78).first().title
#
# user_test = db_session.query(User_Flask).filter(User_Flask.id==6).first()
#
# user_have_books = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().name
# # print(user_have_books)
# book_in_library = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==0).all()
#
# #Какие книги находятся у Виктории?
# book_vik = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first().books
# #Выдадим Виктории книгу Стивена Кинга
# # book_vik_add = db_session.query(User_Flask).filter(User_Flask.name=='Виктория').first() #Виктория
# # King = db_session.query(Library_Flask).filter(Library_Flask.author=='Стивен Кинг').first() #Кинг
# # book_vik_add.books.extend([King]) if King.user_book_id is None else ...#Выдаем
# # db_session.commit() #Сохраняем изменения в БД
#
#
# #Какие книги в библиотеке?
# all_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==None).all()
#
#
# #Каких в библиотеке нет?
#
# # not_books = [book.user_book_id for book in db_session.query(Library_Flask).all()]
# not_books = db_session.query(Library_Flask).filter(Library_Flask.user_book_id==None).all()
# # print(f'В библиотеке сейчас следущие книги:\n')
# # for book in not_books:
# #     print(book.title)
# #Какие читатели взяли хотя бы одну книгу?
#
#
#
# #добавить кингу в библиотеку
# last_number = db_session.query(Library_Flask).order_by(Library_Flask.id.desc()).all()[0].personal_number
# print(last_number)
# # выше обратная сортировка таблицы(order_by(Library_Flask.id.desc())), вывод списка всех результатов, дальше индекс а потом атрибут
#
# test_book = Library_Flask(title='title test',
#                           author='title author',
#                           year='title year',
#                           is_checked_out=1,
#                           personal_number = last_number + 1,
#                           user_book_id = None) # создаем книгу
# # db_session.add_all([test_book]) # добавляем в бд
# # db_session.commit()# коммитим
# counts = {
#
# }
# #подсчет элементов в таблицу по элементу столбца "в данном случае по названию книги"
# lines_title = db_session.query(func.count(Library_Flask.id).filter(Library_Flask.title == 'Джон Картер на Марсе')).scalar()
#
# #порядковый номер последнего элемента
# last_number = db_session.query(Library_Flask).order_by(Library_Flask.personal_number.desc()).first().personal_number
#
# bookkk = db_session.query(Library_Flask).filter(Library_Flask.id==-1).first()
# #выбор всех id и приведение их к нормальному виду
# all_id = list(map(lambda id_book: str(list(id_book)[0]), db_session.query(Library_Flask.id).all()))
#
#
#
# book_on_hand = db_session.query(Library_Flask).filter(Library_Flask.personal_number==58900).first()
# print(book_on_hand)
# # books = db_session.query(Library_Flask).all()
# #
# # users = db_sessionquery(User_Flask).all()
# # for i in users:
# #     print(i)


# АЛЕМБИК. Чтобы эта дичь нормально работала делаем следующее:

# 1. Если мы базу еще не создали. Базу мы создаем с помощью питоновского sqlite
# Прописываем connect = sqlite3.connect('Library_Database_Flask')
#            cursor = connect.cursor() или что то аналогичное


# 2. Дальше работаем уже только с помощью sqlalchemy. Подключаемся к созданной базе, делаем движок и тд(выше пример)
#   Прописываем таблицы через ООП. Каждая таблица - это модель. Прописываем все настройки.
# Если база уже была создана, то мы делаем тоже самое, только классы таблиц будут уже не создавать таблицы, а иметь только
# информационную пользу и будут юзаться алембиком для создания миграций. В любом случае, в них мы всегда должны описывать таблицу


# 3.Устанавливаем алембик PIP

# 4. Создаем файлик session. Из нашего модуля с таблицами SQLalchemy импортируем туда класс Base
# Затем создаем функцию, импортируем оставшиеся модели из модуля с таблицами SQLAlchemy и возвращаем Base


# 5. В файле env.py (который установился вместе с алембиком) прописываем:
# Переходим в директорию с файликом session
# Импортируем функцию, которая возвращает Base
# target_metadata = наша функция().metadata
# и больше ничего не трогаем.


# 6. В файле alembic.ini устанавливаем путь к нашей БД и прописываем настройки:
# script_location = src/migrations -- создает папку для миграций
# prepend_sys_path = . src --- переходит в созданную папку src для взаимодействия со script.py.mako и env.py
# sqlalchemy.url = sqlite:///Library_Database_Flask -- путь к бд SQLITE3


# 7.alembic revision --message='initial' --autogenerate -- запуск тестовой миграции
# Если в ПЕРВОЙ миграции в upgrade и downgrade везде None значит все ок
# alembic upgrade (downgrade) head -- применить самую новую(самую старую) миграции. Если нужна определенная - то вместо
# head пишем ее номер без(_сообщения в ней)

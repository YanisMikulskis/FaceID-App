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

imagePaths = list(paths.list_images('Images'))
knownEncodings, knownNames = [], []
data_faces = {

}
for people_photo in imagePaths:
    name = re.findall(r'([^/\\]+)\.(jpg|jpeg|png|gif|bmp)$', people_photo)[0][0]
    image = cv2.imread(people_photo) # загружаем изображение с помощью cv2
    rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # конвертация в dlib (RGB)
    boxes = face_recognition.face_locations(rgb, model='hog') #находим лица на изображении в dlib формате изображения
    encode_face = face_recognition.face_encodings(rgb, boxes) #создаем эмбендинги лиц в найденном лице на изображении

    # name = re.findall(r'([^/\\]+)\.(jpg|jpeg|png|gif|bmp)$', i)
    # print(name)
    data_faces.setdefault(name, encode_face)

    print()
print(imagePaths)
print(data_faces)
with open('face_enc', 'wb') as faces_file:
    faces_file.write(pickle.dumps(data_faces))
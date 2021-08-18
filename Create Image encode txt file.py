import pickle
import os
import cv2
import face_recognition
# Load the image data set
folder_name = 'ImageData'
images = []
knownNames = []
encodeList = []
name_list = os.listdir(folder_name)
# print(my_list)
for name in name_list:
    curImg = cv2.imread(f'{folder_name}/{name}')
    images.append(curImg)
    knownNames.append(os.path.splitext(name)[0])
for img in images:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(img)[0]
    encodeList.append(encode)
data = {"encodings": encodeList, "names": knownNames}
f = open("face_encode.txt", "wb")
f.write(pickle.dumps(data))

import cv2
import numpy as np
import face_recognition
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pyttsx3
#Text To Speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice', voices[1 ].id)
# rate = engine.getProperty('rate')   # getting details of current speaking rate
# print(rate)                        #printing current voice rate
engine.setProperty('rate', 150)

def speak(audio):  #here audio is var which contain text
    engine.say(audio)
    engine.runAndWait()

URL = 'https://drive.google.com/file/d/18Gv3t_PrR8ialptERtA-In14xPJhDnY5/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+URL.split('/')[-2]
df = pd.read_pickle(path)
known_face_encodings = np.array(df["encodings"])
known_face_names= df["names"]
def markattendance(name):
    now = datetime.now()
    time = now.strftime('%H:%M:%S')
    date = now.strftime("%x")
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    creds = ServiceAccountCredentials.from_json_keyfile_name("GoogleSheet.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("attendance").sheet1
    data = sheet.get_all_records()
    num = len(data)
    col = sheet.col_values(1)
    col2 = sheet.col_values(3)
    if name not in col:
        speak(f"Present{name}")
        insertRow = [name,time,date]
        sheet.insert_row(values=insertRow, index=num + 2)
    elif name in col:
        if date not in col2:
            speak(f"present{name}")
            insertRow = [name, time, date]
            sheet.insert_row(values=insertRow, index=num + 2)
        if date in col2 :
            speak("You are already present today.")


#capture the video
speak("Ready for attendance")
cap = cv2.VideoCapture(0)
while True:
    # Grab a single frame of video
    ret, frame = cap.read()

    #Resize frame of video to 1/4 size for faster face recognition processing
    small_frame_imgs = cv2.resize(frame,(0,0),dst=None, fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame_img = cv2.cvtColor(small_frame_imgs, cv2.COLOR_BGR2RGB)

    #Find all the faces in the current frame of video
    find_faces_current_frame = face_recognition.face_locations(rgb_small_frame_img)

    #encoding the found image
    encode_current_frame = face_recognition.face_encodings(rgb_small_frame_img,find_faces_current_frame)
    for encodeFace, faceLoc in zip(encode_current_frame,find_faces_current_frame):
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings,encodeFace)
        name = "Unknown"
        #use the known face with the smallest distance to the new face
        faceDis = face_recognition.face_distance(known_face_encodings,encodeFace)
        matchIndex = np.argmin(faceDis)
        if matches[matchIndex]:
            name = known_face_names[matchIndex].upper()
            # print(name)

            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4

            # Draw a box around the face
            cv2.rectangle(frame,(x1,y1,),(x2,y2),(0,255,0), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name,(x1+6,y2-6),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)
            markattendance(name)

    # Display the resulting image
    cv2.imshow('Video',frame)
    # cv2.waitKey(1)
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release handle to the webcam
cap.release()
cv2.destroyAllWindows()
# Video Processing with GUI

import os
import cv2
import numpy as np
import PySimpleGUI as sg

cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')

def main():

    #### GUI Part #####
    sg.theme("LightBlue")

    # Define the window layout
    layout = [
        [sg.Text("Video Processing", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")],
        
        # None / FaceDetect / Find Corner
        [sg.Radio("None", "Radio", True, size=(10, 1)),sg.Radio("Face Detect", "Radio", size=(13, 1), key="-FaceDetect-"),sg.Radio("Find Corner", "Radio", size=(10, 1), key="-FindCorner-")],

        #threshold
        [
            sg.Radio("threshold", "Radio", size=(10, 1), key="-THRESH-"),
            sg.Slider(
                (0, 255),
                128,
                1,
                orientation="h",
                size=(40, 15),
                key="-THRESH SLIDER-",
            ),
        ],
        
        #blur
        [
            sg.Radio("blur", "Radio", size=(10, 1), key="-BLUR-"),
            sg.Slider(
                (1, 11),
                1,
                1,
                orientation="h",
                size=(40, 15),
                key="-BLUR SLIDER-",
            ),
        ],

        #hue
        [
            sg.Radio("hue", "Radio", size=(10, 1), key="-HUE-"),
            sg.Slider(
                (0, 225),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-HUE SLIDER-",
            ),
        ],

        [sg.Button("Exit", size=(10, 1))],

    ]

    # Create the window and show it without the plot
    window = sg.Window('Video Processor', layout)
    
    cap = cv2.VideoCapture(0)
    
    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        ret, frame = cap.read()

        if values["-THRESH-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)[:, :, 0]
            frame = cv2.threshold(
                frame, values["-THRESH SLIDER-"], 255, cv2.THRESH_BINARY
            )[1]
            
        #Face and Eye detect
        elif values["-FaceDetect-"]:
            
            faceXML = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            eyeXML = cv2.CascadeClassifier('haarcascade_eye.xml')
    
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = faceXML.detectMultiScale(gray)
            for(x, y, w, h) in faces:
                cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]
                eyes = eyeXML.detectMultiScale(roi_gray)
                for(ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (255,255,0), 2)

            k = cv2.waitKey(27) & 0xFF
            if(k == 27):
                break

        #Find Corner
        elif values["-FindCorner-"]:
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = np.float32(gray)
            corners = cv2.goodFeaturesToTrack(gray,10,0.1,10)
            corners = np.int0(corners)
            
            for corner in corners:
                x, y = corner.ravel()
                cv2.circle(frame, (x,y), 3, (0,255,255), 1)

            k = cv2.waitKey(27) & 0xFF
            if(k == 27):
                break
            
        #BLUR
        elif values["-BLUR-"]:
            frame = cv2.GaussianBlur(frame, (21, 21), values["-BLUR SLIDER-"])

        #HUE
        elif values["-HUE-"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            frame[:, :, 0] += int(values["-HUE SLIDER-"])
            frame = cv2.cvtColor(frame, cv2.COLOR_HSV2BGR)


        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)


    window.close()
main()

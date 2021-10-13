# Final project with GUI

# import libraries
import os
import cv2
import numpy as np
import PySimpleGUI as sg

# library for Extract MP3 audio from Videos
from moviepy.editor import *

# library for Convert Mp3 audio to Text
import speech_recognition as sr

# Import the required module for text to speech conversion
import PyPDF2 
import pyttsx3 

# import XML file for face detect
cv2_base_dir = os.path.dirname(os.path.abspath(cv2.__file__))
haar_model = os.path.join(cv2_base_dir, 'data/haarcascade_frontalface_default.xml')

##============================
def video_to_mp3(file_name):
    audio_file = "Audio.mp3"
    videoClip = VideoFileClip(file_name)
    audioClip = videoClip.audio
    audioClip.write_audiofile(audio_file)
    audioClip.close()
    videoClip.close()
##============================   
def football_processing(video_file,color_a,color_b):
    vidcap = cv2.VideoCapture(video_file)
    success,image = vidcap.read()
    count = 0
    success = True
    idx = 0
    #Read the video frame by frame
    while success:
	#converting into hsv image
        hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
    	#green range
        lower_green = np.array([40,40, 40])
        upper_green = np.array([70, 255, 255])
	
	#blue range
        lower_blue = np.array([110,50,50])
        upper_blue = np.array([130,255,255])

	#red range
        lower_red = np.array([0,31,255])
        upper_red = np.array([176,255,255])

	#white range
        lower_white = np.array([0,0,0])
        upper_white = np.array([0,0,255])
        
        if(color_a == 'blue'):
            upper_a = upper_blue
            lower_a = lower_blue
        elif(color_a == 'red'):
            upper_a = upper_red
            lower_a = lower_red
        elif(color_a == 'green'):
            upper_a = upper_green
            lower_a = lower_green
        elif(color_a == 'white'):
            upper_a = upper_white
            lower_a = lower_white

        if(color_b == 'blue'):
            upper_b = upper_blue
            lower_b = lower_blue
        elif(color_b == 'red'):
            upper_b = upper_red
            lower_b = lower_red
        elif(color_b == 'green'):
            upper_b = upper_green
            lower_b = lower_green
        elif(color_b == 'white'):
            upper_b = upper_white
            lower_b = lower_white
	
	#Define a mask ranging from lower to uppper
        mask = cv2.inRange(hsv, lower_green, upper_green)
	
        #Do masking
        res = cv2.bitwise_and(image, image, mask=mask)
	
	#convert to hsv to gray
        res_bgr = cv2.cvtColor(res,cv2.COLOR_HSV2BGR)
        res_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)

        #Defining a kernel to do morphological operation in threshold image to 
        #get better output.
        kernel = np.ones((13,13),np.uint8)
        thresh = cv2.threshold(res_gray,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	
        #find contours in threshold image     
        contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	
        prev = 0
        font = cv2.FONT_HERSHEY_SIMPLEX

        for c in contours:
                x,y,w,h = cv2.boundingRect(c)
		
		#Detect players
                if(h>=(1.5)*w):
                        if(w>15 and h>= 15):
                                idx = idx+1
                                player_img = image[y:y+h,x:x+w]
                                player_hsv = cv2.cvtColor(player_img,cv2.COLOR_BGR2HSV)
				
                                #If player has color_a jersy
                                mask1 = cv2.inRange(player_hsv, lower_a, upper_a)
                                res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
                                res1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
                                res1 = cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)
                                nzCount = cv2.countNonZero(res1)
				
				#If player has color_b jersy
                                mask2 = cv2.inRange(player_hsv, lower_b, upper_b)
                                res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
                                res2 = cv2.cvtColor(res2,cv2.COLOR_HSV2BGR)
                                res2 = cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
                                nzCountred = cv2.countNonZero(res2)

                                if(nzCount >= 20):
					#Mark blue jersy players as france
                                        cv2.putText(image, color_a, (x-2, y-2), font, 0.8, (255,0,0), 2, cv2.LINE_AA)
                                        cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),3)
                                else:
                                        pass
                                if(nzCountred>=20):
					#Mark red jersy players as belgium
                                        cv2.putText(image, color_b, (x-2, y-2), font, 0.8, (0,0,255), 2, cv2.LINE_AA)
                                        cv2.rectangle(image,(x,y),(x+w,y+h),(0,0,255),3)
                                else:
                                        pass
				    
                if((h>=1 and w>=1) and (h<=30 and w<=30)):
                        player_img = image[y:y+h,x:x+w]
		
                        player_hsv = cv2.cvtColor(player_img,cv2.COLOR_BGR2HSV)
                        #white ball  detection
                        mask1 = cv2.inRange(player_hsv, lower_white, upper_white)
                        res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
                        res1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
                        res1 = cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)
                        nzCount = cv2.countNonZero(res1)
	

                        if(nzCount >= 3):
                                # detect football
                                cv2.putText(image, 'football', (x-2, y-2), font, 0.8, (0,255,0), 2, cv2.LINE_AA)
                                cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),3)


        cv2.imwrite("./Cropped/frame%d.jpg" % count, res)
        print ('Read a new frame: ', success)     # save frame as JPEG file	
        count += 1
        cv2.imshow('Match Detection',image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        success,image = vidcap.read()
    
    vidcap.release()
    cv2.destroyAllWindows()
##============================
def audio_to_text(file_name):
    recognizer = sr.Recognizer()
    
    #recording the sound
    with sr.AudioFile(file_name) as source:
        recorded_audio = recognizer.listen(source)
        print("Done recording")

    #Recorgnizing the Audio
    try:
        print("Recognizing the text")
        text = recognizer.recognize_google(
                recorded_audio, 
                language="en-US"
            )
        #print("Decoded Text : {}".format(text))
        return text
    
    except Exception as ex:
        print(ex)
##============================
def edge_detection(video_file):
    cap = cv2.VideoCapture(video_file)

    while(1):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = np.float32(gray)
        corners = cv2.goodFeaturesToTrack(gray,50,0.1,10)
        corners = np.int0(corners)
                
        for corner in corners:
            x, y = corner.ravel()
            cv2.circle(frame, (x,y), 10, (0,255,255), 1)

        cv2.imshow('Edges', frame)
        
        k = cv2.waitKey(27) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
##============================
def face_detection(video_file):
    cap = cv2.VideoCapture(video_file)
    faceXML = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    while(1):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceXML.detectMultiScale(gray)
        for(x, y, w, h) in faces:
            cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]

        cv2.imshow('Faces', frame)
        
        k = cv2.waitKey(27) & 0xFF
        if k == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
##============================
def PDF_to_Audio(file_name,num):
    # path of the PDF file 
    path = open(file_name, 'rb') 

    # creating a PdfFileReader object 
    pdfReader = PyPDF2.PdfFileReader(file_name) 
  
    # the page with which you want to start  
    from_page = pdfReader.getPage(num-1) 
      
    # extracting the text from the PDF 
    text = from_page.extractText()
    
    # reading the text
    speak = pyttsx3.init() 
    speak.say(text) 
    speak.runAndWait()
##============================
def main():

    #### GUI Part #####
    sg.theme("DarkGrey2")

    # Define the window layout
    layout = [
        [sg.Text('Video File'),sg.Input(),sg.FileBrowse(),
         sg.Checkbox('MP4')],
        
        [sg.Text('Audio File'),sg.Input(),sg.FileBrowse(),
         sg.Checkbox('MP3'), sg.Checkbox('WAV')],
        
        [sg.Text('PDF File  '),sg.Input(),sg.FileBrowse()],

        ##============================  Video Processing (GUI)
        [sg.Text("Video Processing :", size=(60, 1), justification="center")],
        
        # None / FaceDetect / Find Corner
        [sg.Radio("None", "Radio", True, size=(10, 1)),sg.Radio("Face Detect", "Radio", size=(13, 1), key="-FaceDetect-"),sg.Radio("Find Corner", "Radio", size=(10, 1), key="-FindCorner-")],

        #Player Detection
        [
            sg.Radio("Processing of Football Video", "Radio", size=(25, 1), key="-PLAYERDETECTION-"),sg.Text('Color A'),sg.Input(size=(8, 1)) ,sg.Text('Color B'),sg.Input(size=(8, 1))
        ],
        
        #Video to mp3
        [
            sg.Radio("Convert Video to Mp3", "Radio", size=(25, 1), key="-V2M-"),
        ],

        ##============================  Audio Processing (GUI)
        [sg.Text("Audio Processing :", size=(60, 1), justification="center")],
        
        #PDF to mp3
        [
            sg.Radio("Convert PDF to Audio", "Radio", size=(17, 1), key="-P2M-"),
            sg.Slider(
                (1, 200),
                1,
                1,
                orientation="h",
                size=(40, 15),
                key="-P2M SLIDER-",
            ),
        ],
       
        #Audio to Text
        [
            sg.Radio("Convert Audio to Text", "Radio", size=(20, 1), key="-M2T-"),
        ],
        
        ##============================
        [sg.Button('Ok',size=(3, 1)), sg.Button('Cancel',size=(5, 1))]
    ]

    # Create the window and show it without the plot
    window = sg.Window('Converter', layout)
    valid = False
    
    while True:
        event, values = window.read()
        # Here we read the path of the Video file
        video_file = values[0]
        
        if event in (None, 'Cancel'):	# if user closes window or clicks cancel
            print("Exitting")            
            window.close()
            exit()
            break

        if event == "Ok":
            ##============================ Video Processing
            
            #Face Detect
            if values["-FaceDetect-"]:
                if values[1] == True:
                    face_detection(video_file)
                else:
                    print ('Cant support this format')

            #Find Corner
            elif values["-FindCorner-"]:
                if values[1] == True:
                    edge_detection(video_file)
                else:
                    print ('Cant support this format')
            
            #Player Detection   
            elif values["-PLAYERDETECTION-"]:
                if values[1] == True:
                    football_processing(video_file,values[7],values[8])
                else:
                    print ('Cant support this format')
                
            #Video to mp3
            elif values["-V2M-"]:
                if values[1] == True:
                    video_to_mp3(video_file)
                else:
                    print ('Cant support this format')
                
                
            ##============================  Audio Processing
                
            #PDF to Audio
            elif values["-P2M-"]:
               PDF_to_Audio(values[5],int(values["-P2M SLIDER-"]))
                
            #Audio to Text
            elif values["-M2T-"]:
                if values[4] == True:
                    text = audio_to_text(values[2])
                    print("Decoded Text : {}".format(text))
                    with open('audio.txt', 'w') as f:
                        f.write(text)
                else:
                    print ('Cant support this format')
            
main()

import speech_recognition as sr
import sounddevice as sd
import numpy as np
from fuzzywuzzy import process
import json
import pyttsx3
import cv2
import mediapipe as mp
import threading
import os
from pyfirmata import Arduino
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture('http://192.168.1.16:8080/video')
#Penting !!
NeuralNetwork_dir = 'NeuralNetwork\\NeuralNetwork.json'
#Penting !!

try:
    board = input('ArduinoPORT(Leave empty if doesnt exist): ')
    board = Arduino(board)
    pin_9 = board.digital[int(input('PIN: '))]
    pin_9.write(0)
    w_arduino = True
except:
    print('No Arduino Specified')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
mpdraw = mp.solutions.drawing_utils
mpdrawface = mp.solutions.drawing_utils
mpdraw_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands
mpfaces = mp.solutions.face_mesh
mpface_faces = mpfaces.FaceMesh(refine_landmarks=True)
hands = mphands.Hands()
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()
engine = pyttsx3.init()

def Vision():
    global want
    want = False
    while True:
        data, frame = cap.read()
        if not data:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.5, 3)
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
            cv2.putText(frame, 'Human', (x,y-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mpdraw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mphands.HAND_CONNECTIONS
                )


        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_results = mpface_faces.process(frame)
        inverted = cv2.flip(frame.shape, 1)
        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mpdrawface.draw_landmarks(
                    frame,
                    face_landmarks,
                    mpfaces.FACEMESH_CONTOURS,
                    None
                )
                for idx, lm in enumerate(face_landmarks.landmark):
                    w,h,_ = frame.shape
                    x,y = int(lm.x * h), int(lm.y * w)
                    if idx == 1:
                        #try:
                        #    pin_9.write(x / 4)
                        #except:
                        #    pass
                        cv2.putText(frame, 'Communicating with..', (x,y+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = holistic.process(image_rgb)
        if results.pose_landmarks:
            mpdraw.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
        if want == True: 
            cv2.imshow('Computer_Vision', cv2.resize(frame,(800,600)))
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                want = False

t = threading.Thread(target=Vision)
t.start()
recognition = sr.Recognizer()

def voice_input():
    sample_rate = 16000
    duration = 5
    audio_data = sd.rec(int(sample_rate * duration), channels=1, samplerate=sample_rate, dtype='float32')
    sd.wait()

    print('...')
    audio_data = (audio_data * 32767).astype(np.int16)
    audio_data = audio_data.tobytes()

    audio = sr.AudioData(audio_data, sample_rate, 2)

    try:
        text = recognition.recognize_google(audio)
        return text
    except:
        return 'test'

class DeepQLearning:
    def __init__(self, data_file=NeuralNetwork_dir):
        self.Source = data_file
        self.load_knowledge()

    def load_knowledge(self):
        try:
            with open(self.Source, 'r') as file:
                self.knowledge = json.load(file)
        except:
            self.knowledge = {}

    def save_knowledge(self):
        with open(self.Source, 'w') as file:
            json.dump(self.knowledge, file)

    def Best_Match(self, question):
        questions = list(self.knowledge.keys())
        if not questions:
            return None
        if not question == 'test':
            best_match, score = process.extractOne(question, questions)
            if score > 80:
                return self.knowledge[best_match]
        else:
            return '...'
        
    def get_response(self, question):
        response = self.Best_Match(question)
        if response:
            return response
        else:
            return self.learn_new_knowledge(question)
        
    def learn_new_knowledge(self, question):
        #answer = input('How do i answer to something similar to that question in the future? : ')
        #self.knowledge[question] = answer
        #self.save_knowledge()
        return 'I cant seem to answer that question! Feel free to tweak my Network.'
    
gpt_name = 'GPT-2'

if __name__ == '__main__':
    gpt = DeepQLearning()
    while True:
        try:
            mem_size = os.path.getsize(NeuralNetwork_dir)
            mem_size = mem_size / 1024
            print(f'Space Used in NeuralNetwork: {mem_size:.2f} KB.')
            print('Listening..')
            source_input = voice_input()
            print('Translating.. [Using Internet Connections]')
            optimised = '...'
            if not voice_input == '...':
                optimised = gpt.get_response(source_input)
                if not optimised == '...':
                    print(f'{gpt_name} >> {optimised}')
                    engine.say(optimised)
                    engine.runAndWait()
            if optimised == "I can show you right now!..":
                engine.say("This is what I'm seeing..")
                engine.runAndWait()
                want = True
            if optimised == 'Alright closing Computer Vision..':
                try:
                    engine.say(optimised)
                    engine.runAndWait()
                    want = False
                except:
                    print('Error - 101')
            if optimised == 'Okay! Turning off light..':
                pin_9.write(0)
            if optimised == 'Okay! Turning on light..':
                pin_9.write(1)
        except:
            pass

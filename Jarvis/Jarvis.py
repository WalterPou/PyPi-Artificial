import json
import sounddevice as sd
import speech_recognition as sr
import numpy as np
import pyttsx3
import winsound
import pyfirmata as pyf
import pyautogui
import mss
import cv2
import time
import os

sct = mss.mss()
monitor = sct.monitors[1]
template = cv2.imread('RedDot.png', 0)
w, h = template.shape[::-1]

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
try:
    IDX = int(input('COM: '))
    board = pyf.Arduino(f'COM{IDX}')
    pin_9 = board.get_pin('d:9:o')
except:
    pass

class BMA:
    def levenshtein_distance(self,s1,s2):
        if len(s1)<len(s2):
            return self.levenshtein_distance(s2,s1)
        if len(s2)==0:
            return len(s1)
        prev=range(len(s2)+1)
        
        for i,c1 in enumerate(s1):
            current=[i+1]
            for j,c2 in enumerate(s2):
                insert=prev[j+1]+1
                delete=current[j]+1
                subs=prev[j]+(c1!=c2)
                current.append(min(insert,delete,subs))
            prev=current
        return prev[-1]

    def ratio(self,s1,s2):
        distance=self.levenshtein_distance(s1,s2)
        maxLen=max(len(s1),len(s2))
        return 1-distance/maxLen

    def response_data(self,userInput,choices):
        bestMatch=None
        bestScore=-1
        for choice in choices:
            score=self.ratio(userInput,choice)
            if score>bestScore:
                bestMatch=choice
                bestScore=score
        return bestMatch,bestScore


def WakeCall():
    while True:
        sample_rate = 16000
        duration = 3
        print('...')
        audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, dtype='float32', channels=1)
        sd.wait()

        print('Processing')
        audio_data = (audio_data * 32767).astype(np.int16)
        audio_data = audio_data.tobytes()
        audio = sr.AudioData(audio_data, sample_rate, 2)
        try:
            text = sr.Recognizer().recognize_google(audio)
            if text == 'Josh' or 'yo Josh' or 'hey Josh' or 'hello Josh':
                winsound.Beep(750, 150)
                winsound.Beep(1000, 150)
                return 'IDX0'
        except:
            pass
    

def Voice_Input(dur):
    sample_rate = 16000
    duration = dur
    engine.say("I am listening..")
    engine.runAndWait()
    audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, dtype='float32', channels=1)
    sd.wait()

    print('Processing')
    audio_data = (audio_data * 32767).astype(np.int16)
    audio_data = audio_data.tobytes()
    audio = sr.AudioData(audio_data, sample_rate, 2)
    try:
        text = sr.Recognizer().recognize_google(audio)
        return text
    except:
        return "..."
    
class JarvisArtificial:
    def __init__(self, data_file='Network.json'):
        self.Source = data_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.Source, 'r') as Source:
                self.knowledge = json.load(Source)
        except:
            self.knowledge = {}
    
    def save_data(self):
        with open(self.Source, 'w') as Source:
            json.dump(self.knowledge, Source)

    def compare(self, question):
        questions = list(self.knowledge.keys())
        if not question:
            return None
        matches, threshold = BMA().response_data(question, questions)
        if threshold > .2:
            print(f'Question Threshold: {threshold:.2f}')
            return self.knowledge[matches]
        
    def get_response(self, question):
        response = self.compare(question=question)
        if response:
            return response
        else:
            return '...'
        
AI = JarvisArtificial()

def Acc():
    last_move_time = time.time()
    move_interval = 0.03
    while True:
        screenshot = sct.grab(monitor)
        os.system('echo Bypassing Game %TIME%')
        frame = np.array(screenshot)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        if max_val >= threshold:
            
            best_x = max_loc[0] + w // 2
            best_y = max_loc[1] + h // 2

            current_time = time.time()
            if current_time - last_move_time >= move_interval:
                pyautogui.moveTo(best_x, best_y, duration=0.03) 
                last_move_time = current_time
                pyautogui.leftClick()

            cv2.rectangle(frame, max_loc, (max_loc[0] + w, max_loc[1] + h), (0, 255, 0), 2)
            cv2.putText(frame, '?', (max_loc[0], max_loc[1]-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,255), 2)

        cv2.imshow('Bot is visualizing your screen..', cv2.resize(frame, (600,400)))
        #cv2.imshow('Bypassing Game Window..', cv2.Canny(cv2.resize(frame, (600,400)), 100,200))
        if cv2.waitKey(1) == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    while True:
        WakeUp = WakeCall()
        if WakeUp == 'IDX0':
            VoiceData = Voice_Input(7)
            print(VoiceData)
            if VoiceData == 'open device manager':
                engine.say('Right away sir! Opening device manager..')
                engine.runAndWait()
                os.system('devmgmt.msc')
            elif VoiceData == 'create me a file':
                engine.say('Right away sir! Creating a base64 file..')
                engine.runAndWait()
                os.system('type nul > C:\\Users\\User\\Desktop\\File.txt')
            elif VoiceData == 'start searching':
                engine.say('What would you like me to search?')
                engine.runAndWait()
                data = Voice_Input(10)
                engine.say(f'Right away sir! Searching for "{data}"')
                engine.runAndWait()
                data = data.replace(' ', '+')
                os.system(f'start https:\\google.com\\search?q={data}')
            elif VoiceData == 'initiate Target accuracy procedure':
                engine.say(f'Okay Sir! Visualizing screen..')
                engine.runAndWait()
                Acc()
            elif VoiceData == 'start a website':
                engine.say(f'What website would you like me to open?')
                engine.runAndWait()
                data = Voice_Input(5)
                engine.say(f'Right away sir! opening "{data}"')
                engine.runAndWait()
                os.system(f'start https://{data}')
            else:
                response = AI.get_response(VoiceData)
                print(f'> {response}')
                engine.say(response)
                engine.runAndWait()
                if response == 'Okay! Turning on light..':
                    try:
                        pin_9.write(1)
                    except:
                        pass
                elif response == 'Okay! Turning off light..':
                    try:
                        pin_9.write(0)
                    except:
                        pass

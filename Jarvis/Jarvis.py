import json
from fuzzywuzzy import process
import sounddevice as sd
import speech_recognition as sr
import numpy as np
import pyttsx3
import winsound
import pyfirmata as pyf

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
IDX = int(input('COM: '))
board = pyf.Arduino(f'COM{IDX}')
pin_9 = board.get_pin('d:9:o')

def WakeCall():
    while True:
        sample_rate = 16000
        duration = 5
        print('...')
        audio_data = sd.rec(int(sample_rate * duration), samplerate=sample_rate, dtype='float32', channels=1)
        sd.wait()

        print('Processing')
        audio_data = (audio_data * 32767).astype(np.int16)
        audio_data = audio_data.tobytes()
        audio = sr.AudioData(audio_data, sample_rate, 2)
        try:
            text = sr.Recognizer().recognize_google(audio)
            if text == 'hey Jarvis':
                winsound.Beep(750, 150)
                winsound.Beep(1000, 150)
                return 'IDX0'
        except:
            pass
    

def Voice_Input():
    sample_rate = 16000
    duration = 5
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
        return "I'm sorry, I could'nt answer that."
    
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
        matches, threshold = process.extractOne(question, questions)
        if threshold > 80:
            return self.knowledge[matches]
        
    def get_response(self, question):
        response = self.compare(question=question)
        if response:
            return response
        else:
            return '...'
        
AI = JarvisArtificial()

if __name__ == '__main__':
    while True:
        WakeUp = WakeCall()
        if WakeUp == 'IDX0':
            VoiceData = Voice_Input()
            response = AI.get_response(VoiceData)
            print(f'Jarvis >> {response}')
            engine.say(response)
            engine.runAndWait()
            if response == 'Okay! Turning on light..':
                pin_9.write(1)
            elif response == 'Okay! Turning off light..':
                pin_9.write(0)
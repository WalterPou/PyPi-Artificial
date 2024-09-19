import ollama
import pyttsx3
import sounddevice as sd
import speech_recognition as sr
import numpy as np
#import json
#from fuzzywuzzy import process

engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', 200)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def voiceInput(dur):
    sample_rate = 16000
    duration = int(dur)
    print('Listening..')
    data = sd.rec(int(sample_rate * duration), channels=1, dtype='float32', samplerate=sample_rate)
    sd.wait()
    print('Processing..')
    data = (data * 32767).astype(np.int16)
    data = data.tobytes()
    audio = sr.AudioData(data, sample_rate, 2)
    try:
        text = sr.Recognizer().recognize_google(audio)
        return text
    except:
        pass

""" class deviceMgmt:
    def __init__(self, data_file='light.json'):
        self.Source = data_file
        self.load_data()

    def load_data(self):
        try:
            with open(self.Source, 'r') as Source:
                self.knowledge = json.load(self.Source)
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
            self.learn(question)

    def learn(self, question):
        answer = input('How do i answer that? : ')
        self.knowledge[question] = answer
        self.save_data()
     """
class ArtificialIntelligence:
    def __init__(self) -> None:
        self.model='llama3.1'
        self.role='assistant'
        self.maxLength=4000
    
    def get_response(self, question):
        data = ''
        stream = ollama.chat(
        model=self.model,
        messages=[{'role': self.role, 'content': str(question)}],
        options={'num_predict': self.maxLength},
        stream=True
        )
        for chunk in stream:
            data += str(chunk['message']['content'])
        return data
    
if __name__ == '__main__':
    AI = ArtificialIntelligence()
    while True:
        user_input = voiceInput(3)
        if user_input == 'hey Dave':
            engine.say('Im listening.')
            engine.runAndWait()
            user_input = voiceInput(10)
            if user_input:
                response = AI.get_response(user_input)
                print(response)
                engine.say(response)
                engine.runAndWait()
            else:
                engine.say('I could not process the infomation that you provide.')
                engine.runAndWait()
        else:
            pass
import json
from fuzzywuzzy import process

NetworkDIR = r'NeuralNetwork\NeuralNetwork.json'
DeepAI = 'GPT-2'
UserName = 'User'

class DeepQLearning:
    def __init__(self, data_file=NetworkDIR):
        self.memory = data_file
        self.load_mem()

    def load_mem(self):
        try:
            with open(self.memory, 'r') as Source:
                self.knowledge = json.load(Source)
        except:
            self.knowledge = {}

    def save_mem(self):
        with open(self.memory, 'w') as Source:
            json.dump(self.knowledge, Source)

    def best_match(self, question):
        questions = list(self.knowledge.keys())
        if not questions:
            return None
        match, threshold = process.extractOne(question, questions)
        if threshold > 80:
            return self.knowledge[match]
        
    def get_response(self, question):
        response = self.best_match(question)
        if response:
            return response
        else:
            self.learn_mem(question)

    def learn_mem(self, question):
        answer = input('How do i answer to something similar to that question? : ')
        self.knowledge[question] = answer
        self.save_mem()
        return 'Thanks for teaching me!'
    
if __name__ == '__main__':
    DeepBot = DeepQLearning()
    while True:
        prompt = input(f'{UserName}: ')
        if not prompt:
            print('Enter something!')
        else:
            optimised = DeepBot.get_response(prompt)
            print(f'{DeepAI} >> {optimised}')
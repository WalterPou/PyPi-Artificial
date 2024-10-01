import json
import time
import ollama

DeepAI = 'EvilPCT-4'

class levenshteinAlgorithm:
    def levenshteinDistance(self,s1,s2):
        if len(s1)<len(s2):
            return self.levenshteinDistance(s2,s1)
        if len(s2)==0:
            return len(s1)
        previous=range(len(s2)+1)
        for i,a in enumerate(s1):
            current=[i+1]
            #print(current,previous, 'Processing input..')
            #time.sleep(0.001)
            for j,b in enumerate(s2):
                current.append(
                    min(
                        previous[j+1]+1,
                        current[j]+1,
                        previous[j]+(a!=b)
                    )
                )
            previous=current
        return previous[-1]
    
    def levenshteinRatio(self,s1,s2):
        distance=self.levenshteinDistance(s1,s2)
        maxLen=max(len(s1),len(s2))
        return 1-distance/maxLen
    
    def extractOne(self,userInput,choices):
        bestMatch=None
        bestScore=-1
        for choice in choices:
            score=self.levenshteinRatio(userInput,choice)
            #print(choice)
            if score>bestScore:
                bestMatch=choice
                bestScore=score
        #print('\n')
        return bestMatch,bestScore
    
class ArtificialIntel:
    def __init__(self,dataFile='Network.json'):
        self.Source=dataFile
        self.loadData()
        self.model='evil'
        self.role='user'
        self.maxLength=4000

    def loadData(self):
        try:
            with open(self.Source,'r') as Source:
                self.data=json.load(Source)
        except:
            self.data={}

    def saveData(self):
        with open(self.Source,'w') as Source:
            json.dump(self.data,Source)

    def compareData(self,question):
        questions=list(self.data.keys())
        if not question:
            return None
        matches,threshold=levenshteinAlgorithm().extractOne(question,questions)
        print(f'Threshold: {threshold:.2f}\n')
        if threshold>.5:
            return self.data[matches]
        
    def getResponse(self,question):
        response=self.compareData(question)
        if response:
            return response
        else:
            return self.getUnknown(question)
        
    def getUnknown(self,question):
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

AI = ArtificialIntel()

if __name__ == '__main__':
    while True:
        userInput=input('> ')
        response=AI.getResponse(userInput)
        print(f'{DeepAI} > ',end=' ')
        for char in response:
            print(char,end='',flush=True)
            time.sleep(0.03)
        print('\n')

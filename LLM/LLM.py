import json
import random
import time
import os

SourceFile=r'LLM_DataSentence.json'

class BMA:
    def levenshteinDistance(self,s1,s2):
        if len(s1)<len(s2):
            return self.levenshteinDistance(s2,s1)
        if len(s2)==0:
            return len(s1)
        previous=range(len(s2)+1)
        for i,a in enumerate(s1):
            current=[i+1]
            #print(current,previous)
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
    
    def ratio(self,s1,s2):
        distance=self.levenshteinDistance(s1,s2)
        maxLen=max(len(s1),len(s2))
        return 1-distance/maxLen
    
    def extractOne(self,s1,s2):
        bestMatch=None
        bestScore=-1
        for choice in s2:
            score=self.ratio(s1,choice)
            if score>bestScore:
                bestMatch=choice
                bestScore=score
        return bestMatch,bestScore
    
class LLM:
    def __init__(self,dataFile=SourceFile):
        self.Source=dataFile
        self.loadData()
        self.threshold=.6

    def loadData(self):
        try:
            with open(self.Source,'r') as Source:
                self.data=json.load(Source)
        except:
            self.data={}

    def saveData(self):
        with open(self.Source,'w') as Source:
            json.dump(self.data,Source)

    def compareData(self,query):
        questions=list(self.data.keys())
        if not query:
            return None
        matches,threshold=BMA().extractOne(query,questions)
        print(f"Loss: {threshold:.4f}")
        if threshold>self.threshold:
            return self.data[matches]
        else:
            x=list(self.data)
            random.shuffle(x)
            return x[0]

    def responseData(self,query):
        response=self.compareData(query=query)
        if response:
            return response
        else:
            return 'None'

if __name__ == '__main__':
    with open(SourceFile,'r') as Source:
        data=json.load(Source)
    while True:
        os.system('cls')
        inbuffer=list(data.keys())
        random.shuffle(inbuffer)
        oriQuery=inbuffer[0]
        query=list(str(oriQuery))
        random.shuffle(query)
        query=''.join(query)
        outbuffer=LLM().responseData(query)
        print(f'In: {query}\nOut: {outbuffer}\nOriginal In: {oriQuery}\nCorrect Out: {data[str(oriQuery)]}')
        #time.sleep(0.2)
        while outbuffer!=data[str(oriQuery)]:
            x=list(str(query))
            random.shuffle(x)
            #print(x)
            y=''.join(x)
            #print(f'\n{y}',end='\n')
            matches,threshold=BMA().extractOne(y,list(data.keys()))
            outbuffer=matches
            #time.sleep(0.2)
            #for char in outbuffer:
            #    print(char,end='',flush=True)
            #    time.sleep(0.02)
            if outbuffer==oriQuery:
                break
            else:
                #time.sleep(0.2)
                os.system('cls')
                print(f'\nComputed Loss: {threshold}')
                print(f'Computed In: {matches}')
                print(f'Computed Out: {data[str(matches)]}\n')
                print(f'In: {y}\nOut: {outbuffer}\nOriginal In: {oriQuery}\nCorrect Out: {data[str(oriQuery)]}')
                print(f'Loss: {threshold}')
        #time.sleep(3)
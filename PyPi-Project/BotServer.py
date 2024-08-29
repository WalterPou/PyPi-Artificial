import json
from fuzzywuzzy import process
import socket
import threading

h = str(input('H: '))
p = int(input('P: '))
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((h,p))
                     
class ArtificialBrain:
    def __init__(self,data_file='NeuralNetwork\\NeuralNetwork.json'):
        self.Source=data_file
        self.load_data()
    def load_data(self):
        try:
            with open(self.Source,'r') as Source:
                self.knowledge=json.load(Source)
        except:
            self.knowledge={}
    def save_data(self):
        with open(self.Source,'w') as Source:
            json.dump(self.knowledge,Source)
    def best_match(self,question):
        questions=list(self.knowledge.keys())
        if not question:
            return None
        matches,threshold=process.extractOne(question,questions)
        if threshold>80:
            return self.knowledge[matches]
    def get_response(self,question):
        response=self.best_match(question)
        if response:
            return response
        else:
            return 'fix'
    def learn(self,question,alias):
        self.knowledge[question]=alias
        self.save_data()

def handle_client(conn,addr):
    print(f'[Connected] {addr} connected.')
    connected=True
    bot=ArtificialBrain()
    while connected:
        msg=conn.recv(1024).decode()
        if msg=='!DISCONNECT':
            print(f'[DISCONNECTED] {addr} disconnected.')
            connected=False
        else:
            print(f'Received({addr}): {msg}')
            print('Responding..')
            response=bot.get_response(msg)
            if response=='fix':
                conn.sendall('How do i answer that?'.encode())
                data=conn.recv(1024).decode()
                bot.learn(question=msg,alias=data)
                conn.sendall('Thanks for teaching me!'.encode())
            else:
                conn.sendall(response.encode())
    conn.close()

def start():
    server.listen()
    print(f'Server is listening..')
    while True:
        conn,addr=server.accept()
        thread=threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()

start()

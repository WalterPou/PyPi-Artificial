from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders.colored_lights_shader import colored_lights_shader
import ollama
import pyttsx3 as pyt
import threading

app=Ursina()
engine=pyt.init()
Sky()

def read(text):
    engine.say(text)
    engine.runAndWait()

class Voxel(Button):
    def __init__(self,position=(4,2,4),texture='white_cube'):
        super().__init__(
            model='cube',
            texture=texture,
            position=position,
            color=color.rgb(150,150,150),
            collider='box',
            shader=colored_lights_shader,
            parent=scene
        )

    def input(self,key):
        if self.hovered:
            if key == 'right mouse down':
                voxel=Voxel(position=self.position+mouse.normal)
            if key == 'left mouse down':
                destroy(self)

for z in range(20):
    for x in range(20):
        voxel=Voxel(position=(x,-1,z))

class Player(Entity):
    def __init__(self,**kwargs):
        self.player=FirstPersonController(position=(4,2,4))
        super().__init__(parent=self.player)
        window.fullscreen=True
        self.input_active=False
        self.ai_response=Text("AI: ", scale=0.8, position=(-.8,0.4,0), color=color.white)
        #self.ai_response.visible=False
        self.ai_response.visible=True

    def Submit(self):
        query=self.inpl.text
        responseThread=threading.Thread(target=self.fetch_response, args=(query,))
        responseThread.start()

    def fetch_response(self,query):
        response=LLMS().Response(query)
        invoke(self.update_ai_response, response)
        talk=threading.Thread(target=read, args=(response,)).start()

    def update_ai_response(self,response):
        self.ai_response.text="AI: "+response
        print("Response Updated.")

    def input(self,key):
        if key=='`':
            if self.input_active:
                destroy(self.inpl)
                self.input_active=False
                mouse.locked=True
                self.player.enabled=True
                #self.ai_response.visible=False
                print('Deactivated')
            else:
                mouse.locked = False
                self.inpl = InputField()
                self.inpl.y=-.3
                self.inpl.submit_on = 'enter'
                self.inpl.on_submit = self.Submit
                self.input_active = True
                self.player.enabled=False
                #self.ai_response.visible=True
                print("Input box activated!")

class LLMS:
    def __init__(self,model="stablelm-zephyr",role="user"):
        self.model=model
        self.role=role

    def Response(self,query):
        data=''
        stream=ollama.chat(
            model=self.model,
            messages=[{'role': self.role, 'content': str(query)}],
            stream=True
        )
        for chunk in stream:
            data+=str(chunk['message']['content'])
        return data

if __name__ == '__main__':
    Player()
    app.run()

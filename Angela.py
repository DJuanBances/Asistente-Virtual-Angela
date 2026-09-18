import speech_recognition as sr
import subprocess as sub
import pyttsx3,pywhatkit, wikipedia, datetime, keyboard,colores, os
from pygame import mixer
 
name = "Angela"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)

sites ={
            'google': 'google.com',
            'youtube': 'youtube.com',
            'facebook': 'facebook.com',
            'whatsapp': 'web.whatsapp.com',
            'blackboard': 'ucv.blackboard.com',
            'trilce': 'trilce.ucv.edu.pe'      
}

files = {
    'informe':'PPP2-C2-PRA06a-INFORME_PRACTICAS- BANCES VASQUEZ JUAN CARLOS.docx',
    'curriculum':'PPP2-C2-PRA01-CV-BANCES VASQUEZ JUAN CARLOS.docx',
    'indicador':'63 Maestro Comas - Indicador de Merma al 21.08.22.xlsx'
}

programas = {
    'zoom': r"C:\Users\Lenovo\AppData\Roaming\Zoom\bin\Zoom.exe",
    'excel': r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    'word': r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    'chrome': r"C:\Program Files\Google\Chrome\Application\chrome.exe"    
}

contacts ={
            'Andrea': '+51936230023',
            'Kelly': '+51947637104',
            'Enzo': '+51970714090',
            'Papa': '+51980048962',
            'Prof jose luis': '+51970012210'    
}

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def listen():
    try:
        with sr.Microphone() as source:
            print("Escuchando...")
            pc = listener.listen(source)
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()
            if name in rec:
                rec = rec.replace(name, '')
    except:        
        pass
    return rec

def run_Angela():
    while True:
        rec = listen()
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            print(search +": " + wiki)
            talk(wiki)
        elif 'alarma' in rec:
            num = rec.replace('alarma', '')
            num = num.strip()
            talk("Alarma activada a las " + num + " horas")
            while True:
                if datetime.datetime.now().strftime('%H:%M')==num:
                    print("LEVANTATE!!!")
                    mixer.init()
                    mixer.music.load("alarm-clock.mp3")
                    mixer.music.play()
                    if keyboard.read_key() == "s":
                        mixer.music.stop()
                        break
        elif 'colores' in rec:
            talk("Enseguida")
            colores.capture()    
        elif 'abre' in rec:
            for site in sites:
                if site in rec:
                    sub.call(f'start chrome.exe {sites[site]}', shell=True)
                    talk(f'Abriendo {site}')
            for app in programas:
                if app in rec:
                    talk(f'Abriendo {app}')
                    sub.Popen(programas[app])
                            
        elif 'archivo' in rec:
            for file in files:
                if file in rec:
                    sub.Popen([files[file]], shell=True)
                    talk(f'Abriendo {file}')
        elif 'escribe' in rec:
            try:
                with open("nota.txt", 'a') as f:
                    write(f)
                    
            except FileNotFoundError as e:
                file = open("nota.txt", 'a')
                write(file)
                
        elif 'termina' in rec:
            talk('Adios!')
            break
        
def write(f):
    talk("Lista para anotar")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes chequearlo")
    sub.Popen("nota.txt", shell=True)                                                                 
        
if __name__ =='__main__':
    run_Angela()
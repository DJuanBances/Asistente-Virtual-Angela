import speech_recognition as sr
import subprocess as sub
import pyttsx3
import pywhatkit 
import wikipedia 
import datetime 
import keyboard 
import colores 
import os
from tkinter import *
from PIL import Image,ImageTk
from pygame import mixer
import threading as tr
import whatsapp as wsp

main_window = Tk()
main_window.title("Asistente Ángela")

main_window.geometry("800x470")
main_window.resizable(0,0)
main_window.configure(bg='#f953c6')

comandos = """
    Comandos a utlizar:
    - Reproduce.. (cancion)
    - Busca... (algo)
    - Abre... (pagina web o app)
    - Alarma... (hora en 24 HRS)
    - Archivo.. (nombre)
    - Colores... (rojo, azul, amarillo)
    - Mensaje.. (Whatsapp)
    - Termina
    
"""

label_tittle = Label(main_window, text="Asistente Angela", bg="#f4c4f3", fg="#0f0c29",
                     font=('Century Gothic', 30, 'bold'))
label_tittle.pack(pady=10)

canvas_comandos = Canvas(bg="#f4c4f3", height=150, width=190)
canvas_comandos.place(x=0, y=0)
canvas_comandos.create_text(90, 80, text=comandos, fill="black", font='Arial 10')

text_info = Text(main_window, bg="#f4c4f3", fg="black")
text_info.place(x=0, y=150, height=315, width=190 )

Angela_foto = ImageTk.PhotoImage(Image.open("Angela rostro.png"))
window_photo = Label(main_window, image=Angela_foto)
window_photo.pack(pady=5)

def voz_mexicana():
    change_voice(0)
def voz_española():
    change_voice(2)
def voz_americana():
    change_voice(1)
def change_voice(id):
    engine.setProperty('voice', voices[id].id)
    engine.setProperty('rate', 145)
    talk("Hola soy Ángela") 

name = "Angela"
listener = sr.Recognizer()
engine = pyttsx3.init()

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 145)
for voice in voices:
    print(voice)
    

def charge_data(name_dict, name_file):
    try:
        with open(name_file) as f:
            for line in f:
                print(line.split())
                (key, val) = line.split(",")
                val = val.rstrip("\n")
                name_dict[key] = val
    except FileNotFoundError as e:
        pass     

sites = dict()
charge_data(sites, "pages.txt")
files = dict()
charge_data(files, "archivos.txt")
programas = dict()
charge_data(programas, "programs.txt")
contacts = dict()
charge_data(contacts, "contacts.txt")

def talk(text):
    engine.say(text)
    engine.runAndWait()
    
def leer_y_hablar():
    text = text_info.get("1.0","end")
    talk(text)
def write_text(text_wiki):
    text_info.insert(INSERT,text_wiki)       
    
def listen():
    listener = sr.Recognizer()
    with sr.Microphone() as source:
        listener.adjust_for_ambient_noise(source)
        talk("Te escucho")
        pc = listener.listen(source)
    try:
            rec = listener.recognize_google(pc, language="es")
            rec = rec.lower()    
    except sr.UnknownValueError:  
        print("No te entendí, intenta de nuevo")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    return rec

def clock(rec):
    num = rec.replace('alarma', '')
    num = num.strip()
    talk("Alarma activada a las " + num + " horas")
    if num[0] != 0 and len(num) < 5:
        num = '0' + num
    print(num)
    while True:
        if datetime.datetime.now().strftime('%H:%M') == num:
            print("LEVANTATE!!!")
            mixer.init()
            mixer.music.load("alarm-clock.mp3")
            mixer.music.play()
        else:
            continue    
        if keyboard.read_key() == "s":
            mixer.music.stop()
            break
  
def run_Angela():
   while True:
        try:
            rec = listen()
        except UnboundLocalError:
            talk("No te entendí, intenta de nuevo")
            continue    
        if 'reproduce' in rec:
            music = rec.replace('reproduce', '')
            print("Reproduciendo " + music)
            talk("Reproduciendo " + music)
            pywhatkit.playonyt(music)
        elif 'busca' in rec:
            search = rec.replace('busca', '')
            wikipedia.set_lang("es")
            wiki = wikipedia.summary(search, 1)
            talk(wiki)
            write_text(search +": " + wiki)
            break
        elif 'alarma' in rec:
            t = tr.Thread(target=clock, args=(rec,))
            t.start()
        elif 'colores' in rec:
            talk("Enseguida")
            colores.capture()    
        elif 'abre' in rec:
            task = rec.replace('abre', '').strip()
            
            if task in sites:
                for task in sites:
                    if task in rec:
                        sub.call(f'start chrome.exe {sites[task]}', shell=True)
                        talk(f'Abriendo {task}')
            elif task in programas:            
                for task in programas:
                    if task in rec:
                        talk(f'Abriendo {task}')
                        sub.Popen(programas[task])
            else:
                talk("Lo siento, esta aplicación o página web no está agregada, usa los botones de agregar!")            
                                
        elif 'archivo' in rec:
            file = rec.replace('archivo', '').strip()
            if file in files:
                for file in files:
                    if file in rec:
                        sub.Popen([files[file]], shell=True)
                        talk(f'Abriendo {file}')
            else:
                talk("Lo siento, parece que no has agregado ese archivo, usa los botones de agregar!") 
                
        elif 'mensaje' in rec:
            talk("¿A quién quieres enviar el mensaje?")
            contact = listen()
            contact = contact.strip()

            if contact in contacts: 
                for cont in contacts:
                    if cont == contact: 
                        contact = contacts[cont]
                        talk("¿Qué mensaje quieres enviarle?")
                        message = listen()
                        talk("Enviando mensaje..")
                        wsp.send_message(contact,message)
            else:
                talk("Parece que aún no has agregado a ese contacto, usa el boton de agregar.") 
                
        elif 'cierra' in rec:
            for task in sites:
                kill_task = sites[task].split("\\")
                kill_task = kill_task[-1]
                if task in rec:
                    sub.call(f'TASKILL /IM {kill_task} /F', shell=True)
                    talk(f'Cerrando {task}')
                if 'todo' in rec:
                    sub.call(f'TASKILL /IM {kill_task} /F', shell=True) 
                    
            if 'ciérrate' in rec:
                talk(f'Hasta Luego') 
                sub.call('TASKILL /IM python.exe /F', shell=True)
                                
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

main_window.update()
    
def write(f):
    talk("Lista para anotar")
    rec_write = listen()
    f.write(rec_write + os.linesep)
    f.close()
    talk("Listo, puedes chequearlo")
    sub.Popen("nota.txt", shell=True)
    
def abrir_archivos():
    global namefile_entry, pathf_entry
    windows_files = Toplevel()
    windows_files.title("Agregar archivos")
    windows_files.configure(bg="#4b6cb7")
    windows_files.geometry("300x200")
    windows_files.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_files)} center')
    
    title_label = Label(windows_files, text="Agrega un archivo", fg="white", bg="#4b6cb7", font=("Century Gothic", 15, "bold"))
    title_label.pack(pady=3)
    name_label = Label(windows_files, text="Nombre del archivo", fg="white", bg="#4b6cb7", font=("Century Gothic", 10, "bold"))
    name_label.pack(pady=2)
    
    namefile_entry = Entry(windows_files)
    namefile_entry.pack(pady=1)
    
    path_label = Label(windows_files, text="Ruta del archivo", fg="white", bg="#4b6cb7", font=("Century Gothic", 10, "bold"))
    path_label.pack(pady=2)
    
    pathf_entry = Entry(windows_files, width=35)
    pathf_entry.pack(pady=1)
    
    save_button = Button(windows_files, text="Guardar", fg="white", bg="#6f0000", width=9, height=1, command=agregar_archivos)
    save_button.pack(pady=4)
    
def abrir_aplicaciones():
    global nameapps_entry, patha_entry
    windows_apps = Toplevel()
    windows_apps.title("Agregar apps")
    windows_apps.configure(bg="#8E0E00")
    windows_apps.geometry("300x200")
    windows_apps.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(windows_apps)} center')
    
    title_label = Label(windows_apps, text="Agrega una app", fg="white", bg="#8E0E00", font=("Century Gothic", 15, "bold"))
    title_label.pack(pady=3)
    name_label = Label(windows_apps, text="Nombre de la app", fg="white", bg="#8E0E00", font=("Century Gothic", 10, "bold"))
    name_label.pack(pady=2)
    
    nameapps_entry = Entry(windows_apps)
    nameapps_entry.pack(pady=1)
    
    path_label = Label(windows_apps, text="Ruta de la app", fg="white", bg="#8E0E00", font=("Century Gothic", 10, "bold"))
    path_label.pack(pady=2)
    
    patha_entry = Entry(windows_apps, width=35)
    patha_entry.pack(pady=1)
    
    save_button = Button(windows_apps, text="Guardar", fg="white", bg="#1F1C18", width=9, height=1,command=agregar_apps) 
    save_button.pack(pady=4)
    
def abrir_páginas():
    global namepages_entry, pathp_entry
    window_pages = Toplevel()
    window_pages.title("Agregar paginas")
    window_pages.configure(bg="#0f9b0f")
    window_pages.geometry("300x200")
    window_pages.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_pages)} center')
    
    title_label = Label(window_pages, text="Agrega una pagina", fg="white", bg="#0f9b0f", font=("Century Gothic", 15, "bold"))
    title_label.pack(pady=3)
    name_label = Label(window_pages, text="Nombre de la pagina", fg="white", bg="#0f9b0f", font=("Century Gothic", 10, "bold"))
    name_label.pack(pady=2)
    
    namepages_entry = Entry(window_pages)
    namepages_entry.pack(pady=1)
    
    path_label = Label(window_pages, text="Ruta de la pagina", fg="white", bg="#0f9b0f", font=("Century Gothic", 10, "bold"))
    path_label.pack(pady=2)
    
    pathp_entry= Entry(window_pages, width=35)
    pathp_entry.pack(pady=1)
    
    boton_guardar = Button(window_pages, text="Guardar", fg="white", bg="#093028", width=9, height=1, command=agregar_paginas)
    boton_guardar.pack(pady=4)
    
def abrir_contactos():
    global namecontacts_entry, phone_entry
    window_contacts = Toplevel()
    window_contacts.title("Agregar contactos")
    window_contacts.configure(bg="#fd1d1d")
    window_contacts.geometry("300x200")
    window_contacts.resizable(0,0)
    main_window.eval(f'tk::PlaceWindow {str(window_contacts)} center')
    
    title_label = Label(window_contacts, text="Agrega un contacto", fg="white", bg="#fd1d1d", font=("Century Gothic", 15, "bold"))
    title_label.pack(pady=3)
    name_label = Label(window_contacts, text="Nombre del contacto", fg="white", bg="#fd1d1d", font=("Century Gothic", 10, "bold"))
    name_label.pack(pady=2)
    
    namecontacts_entry = Entry(window_contacts)
    namecontacts_entry.pack(pady=1)
    
    phone_label = Label(window_contacts, text="Número celular (Con codigo de país)", fg="white", bg="#fd1d1d", font=("Century Gothic", 10, "bold"))
    phone_label.pack(pady=2)
    
    phone_entry= Entry(window_contacts, width=35)
    phone_entry.pack(pady=1)
    
    boton_guardar = Button(window_contacts, text="Guardar", fg="white", bg="#093028", width=9, height=1, command=agregar_contactos)
    boton_guardar.pack(pady=4)
    
    
def agregar_archivos():
    name_file = namefile_entry.get().strip()
    path_file = pathf_entry.get().strip()
    
    files[name_file] = path_file
    save_data(name_file, path_file, "archivos.txt")
    namefile_entry.delete(0, "end")
    pathf_entry.delete(0, "end")
    
def agregar_apps():
    name_app = nameapps_entry.get().strip()
    path_app = patha_entry.get().strip()
    
    programas[name_app] = path_app
    save_data(name_app, path_app, "apps.txt")
    nameapps_entry.delete(0, "end")
    patha_entry.delete(0, "end")
    
def agregar_paginas():
    name_page = namepages_entry.get().strip()
    url_pages = pathp_entry.get().strip()
    
    sites[name_page] = url_pages
    save_data(name_page, url_pages, "pages.txt")
    namepages_entry.delete(0, "end")
    pathp_entry.delete(0, "end")
    
def agregar_contactos():
    name_contact = namecontacts_entry.get().strip()
    phone = phone_entry.get().strip()
    
    contacts[name_contact] = phone
    save_data(namecontacts_entry, phone, "contacts.txt")
    namecontacts_entry.delete(0, "end")
    phone_entry.delete(0, "end")   
    
def save_data(key, value, file_name):
    try:
        with open(file_name, 'a') as f:
            f.write(key + "," + value + "\n")
    except FileNotFoundError as f:
        file = open(file_name, 'a')
        file.write(key + "," + value + "\n")
        
def talk_pages():
    if bool(sites) == True:
        talk("Has agregado las siguientes páginas web")
        for site in sites:
            talk(site)
    else:
        talk("Aun no has agregado páginas web") 
               
def talk_apps():
    if bool(programas) == True:
        talk("Has agregado las siguientes aplicaciones")
        for app in programas:
            talk(app)
    else:
        talk("Aun no has agregado aplicaciones")
        
def talk_files():
    if bool(files) == True:
        talk("Has agregado los siguientes archivos")
        for file in files:
            talk(file)
    else:
        talk("Aun no has agregado ningun archivo")
        
def talk_contacts():
    if bool(contacts) == True:
        talk("Has agregado los siguientes contactos")
        for cont in contacts:
            talk(cont)
    else:
        talk("Aun no has agregado ningun contacto")
        
def give_me_name():
    talk("Hola, ¿Cómo te llamas?")
    name = listen()
    name = name.strip()
    talk(f"Bienvenido {name}")
    
    try:
        with open("name.txt", 'w') as f:
            f.write(name)
    except FileNotFoundError:
        file = open("name.txt", 'w')
        file.write(name)
        
def say_hello():
    
        if os.path.exists("name.txt"):
            with open("name.txt") as f:
                for name in f:
                    talk(f"Hola, bienvenido {name}")
        else:
            give_me_name()
            
def thread_hello():
    t = tr.Thread(target=say_hello)
    t.start()
    
thread_hello()                             

button_voice_mx = Button(main_window, text="Mexicana", fg="white", bg="#38ef7d", font=("Century Gothic", 10, "bold"), command=voz_mexicana)
button_voice_mx.place(x=570, y=80, width=100, height=30)   
button_voice_es = Button(main_window, text="Española", fg="white", bg="#f12711", font=("Century Gothic", 10, "bold"),command=voz_española)
button_voice_es.place(x=570, y=120, width=100, height=30) 
button_voice_us = Button(main_window, text="Americana", fg="white", bg="#1565C0", font=("Century Gothic", 10, "bold"),command=voz_americana)
button_voice_us.place(x=570, y=160, width=100, height=30)
button_listen = Button(main_window, text="Escuchar", fg="white", bg="#302b63", font=("Century Gothic", 9, "bold"),command=run_Angela)
button_listen.pack(side= BOTTOM, pady=10)
button_speak = Button(main_window, text="Hablar", fg="white", bg="#41295a", font=("Century Gothic", 10, "bold"), command=leer_y_hablar)
button_speak.place(x=570, y=200, width=100, height=30)

button_add_files = Button(main_window, text="Agregar archivos", fg="white", bg="#1CB5E0", font=("Century Gothic", 10, "bold"), command=abrir_archivos)
button_add_files.place(x=590, y=250, width=120, height=30) 
button_add_apps = Button(main_window, text="Agregar aplicaciones", fg="white", bg="#434343", font=("Century Gothic", 10, "bold"), command=abrir_aplicaciones)
button_add_apps.place(x=590, y=290, width=150, height=30) 
button_add_pages = Button(main_window, text="Agregar páginas", fg="white", bg="#870000", font=("Century Gothic", 10, "bold"), command=abrir_páginas)
button_add_pages.place(x=590, y=330, width=120, height=30)
button_add_contacts = Button(main_window, text="Agregar contactos", fg="white", bg="#DA4453", font=("Century Gothic", 10, "bold"), command=abrir_contactos)
button_add_contacts.place(x=590, y=370, width=140, height=30)

button_tell_pages = Button(main_window, text="Páginas agregadas", fg="white", bg="#870000", font=("Century Gothic", 8, "bold"), command=talk_pages)
button_tell_pages.place(x=193, y=350, width=120, height=30,)
button_tell_apps = Button(main_window, text="Apps agregadas", fg="white", bg="#434343", font=("Century Gothic", 8, "bold"), command=talk_apps)
button_tell_apps.place(x=323, y=350, width=120, height=30)
button_tell_files = Button(main_window, text="Archivos agregados", fg="white", bg="#1CB5E0", font=("Century Gothic", 8, "bold"), command=talk_files)
button_tell_files.place(x=453, y=350, width=120, height=30)
button_tell_contacts = Button(main_window, text="Contactos agregados", fg="white", bg="#DA4453", font=("Century Gothic", 8, "bold"), command=talk_contacts)
button_tell_contacts.pack(side= BOTTOM, pady=5)

main_window.mainloop()
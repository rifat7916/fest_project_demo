import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyjokes
import webbrowser
import os
from tkinter import Tk,Label,Scrollbar,Canvas,Frame,VERTICAL

# speech recognition and text-to-speech initialization
listener=sr.Recognizer()
jarvis=pyttsx3.init()
voices=jarvis.getProperty('voices')
jarvis.setProperty('voice',voices[0].id)
HISTORY_FILE="search_history.txt"

# History load hobe
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE,"w")as file:pass  # file exist na thakle create korbe
with open(HISTORY_FILE,"r")as file:history=file.readlines()

# tkinter =window and panel open howar jonno
root=Tk()
root.title("SpeakSmart")
root.geometry("500x400")

canvas=Canvas(root)
scrollbar=Scrollbar(root,orient=VERTICAL,command=canvas.yview)
frame=Frame(canvas)
canvas.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right",fill="y")
canvas.pack(side="left",fill="both",expand=True)
canvas.create_window((0,0),window=frame,anchor="nw")

label_text=Label(frame,text="I'm listening, Sir",font=("Arial",12),anchor="w",justify="left")
label_text.grid(row=0,column=0,sticky="w",padx=10,pady=5)

def update_panel(text,is_command=True):
    # commands or results er sathe panel update kora.
    prefix="● "if is_command else"✔ "
    label=Label(frame,text=f"{prefix}{text}",font=("Arial",12),anchor="w",justify="left")
    label.grid(row=len(frame.winfo_children()),column=0,sticky="w",padx=10,pady=5)
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

def talk(text):
    update_panel(text,is_command=False)  # bolar age likhe print korar jonno
    jarvis.say(text)
    jarvis.runAndWait()

def take_command():
    try:
        with sr.Microphone()as mic:
            listener.adjust_for_ambient_noise(mic,duration=1)  # noise handling
            update_panel("Listening...",is_command=True)
            voice=listener.listen(mic,timeout=5,phrase_time_limit=10)  # hang na korar jonno timeout set korchi
            command=listener.recognize_google(voice).lower()
            if'jarvis'in command:command=command.replace('jarvis','').strip()
            return command
    except sr.UnknownValueError:
        update_panel("Sorry, I didn't catch that. Could you please repeat?",is_command=False)
    except sr.RequestError:
        update_panel("There seems to be an issue with the speech service.",is_command=False)
    except Exception as e:
        update_panel("An error occurred: "+str(e),is_command=False)
    return ""

def save_history(command):
    # search hsitory save korbe and listing korbe.
    if command not in history:
        history.append(command+"\n")
        with open(HISTORY_FILE,"a")as file:file.write(command+"\n")

def run_jarvis():
    # Main function to run jarvis
    talk("I'm listening, Sir")
    def listen_loop():
        command=take_command()
        if command:
            if'stop listening'in command:
                talk("Goodbye, Sir!")
                root.destroy()  # tkinter panel close korbe
                exit()  # program shut down korbe
            elif'time'in command:
                current_time=datetime.datetime.now().strftime('%I:%M %p')
                talk('Current time is '+current_time)
            elif'play'in command:
                song=command.replace('play','').strip()
                talk(f"Playing {song}")
                pywhatkit.playonyt(song)
            elif'tell me about'in command:
                topic=command.replace('tell me about','').strip()
                try:
                    info=wikipedia.summary(topic,1)
                    talk(info)
                    save_history(f"Info about {topic}")
                except Exception:
                    talk(f"Sorry, I could not find information about {topic}")
            elif'joke'in command:
                joke=pyjokes.get_joke()
                talk(joke)
            elif'search'in command:
                query=command.replace('search','').strip()
                talk(f"I'm searching for {query}, Sir")
                pywhatkit.search(query)
                save_history(query)
            elif'search on facebook'in command:
                person=command.replace('search on facebook','').strip()
                url=f"https://www.facebook.com/search/top/?q={person}"
                talk(f"Searching for {person} on Facebook")
                webbrowser.open(url)
                save_history(f"Facebook search: {person}")
            elif'show history'in command:
                if history:
                    talk("Here is your search history, Sir.")
                    for item in history:update_panel(item.strip(),is_command=False)
                else:
                    talk("Your search history is empty, Sir.")
            else:
                talk("I did not get it, but I am going to search it for you.")
                pywhatkit.search(command)
                save_history(command)
        root.after(500,listen_loop)  # listen loop function 0.5 secs pore start hobe
    listen_loop()  # loop er recursion

root.after(100,run_jarvis)  # 0.1 second pore program start korbe
root.mainloop()

import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import webbrowser

listener = sr.Recognizer()
jarvis = pyttsx3.init()
voices = jarvis.getProperty('voices')
jarvis.setProperty('voice', voices[0].id)
contacts = {
    "Mrs. Ahmed": "01836449716",
}

def talk(text):
    jarvis.say(text)
    jarvis.runAndWait()

def take_command():
    try:
        with sr.Microphone() as mic:
            print('listening...')
            voice=listener.listen(mic)
            command=listener.recognize_google(voice)
            command = command.lower()
            if 'jarvis' in command:
                command=command.replace('jarvis', '')
    except:
        pass
    return command

def run_jarvis():
    talk("I'm listening, Sir")
    while True:
        command=take_command()
        if 'stop listening' in command:
            talk("Let me know when you're ready for the next command. Thank you.")
            break
        
        if 'time' in command:
            time=datetime.datetime.now().strftime('%I:%M %p')
            print(time)
            talk('Current time is ' + time)
        
        elif 'play' in command:
            song = command.replace('play', '')
            talk('playing '+ song)
            pywhatkit.playonyt(song)
        
        elif 'tell me about' in command:
            look_for=command.replace('tell me about', '')
            info = wikipedia.summary(look_for, 1)
            print(info)
            talk(info)
        
        
        elif 'search' in command:
            search_query = command.replace('search', '').strip()
            talk(f"I'm searching for {search_query}, Sir")
            pywhatkit.search(search_query)
        
        elif 'search on facebook' in command:
            person=command.replace('search on facebook', '').strip()
            url = f'https://www.facebook.com/search/top/?q={person}'
            talk(f'Searching for {person} on Facebook')
            webbrowser.open(url)
        
        elif 'call' in command:
            name=command.replace('call', '').strip()
            if name in contacts:
                talk(f'Calling {name} on WhatsApp')
                pywhatkit.sendwhatmsg_instantly(contacts[name], '', wait_time=10)
            else:
                talk("Sorry sir, I can't find the contact.")
        
        elif 'text' in command:
            name=command.split('text')[1].split(' ')[0].strip()
            message_start = command.find(f"{name}") + len(name)
            message = command[message_start:].strip()
            if name in contacts:
                talk(f'Sending message to {name}')
                pywhatkit.sendwhatmsg_instantly(contacts[name], message, wait_time=10)
            else:
                talk("Sorry sir, I can't find the contact.")

        
        else:
            talk('I did not get it but I am going to search it for you')
            pywhatkit.search(command)

run_jarvis()

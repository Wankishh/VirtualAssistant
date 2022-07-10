import os
import platform

import pyttsx3
import speech_recognition as sr
import webbrowser as wb

r = sr.Recognizer()

opening_commands = ["run", "open"]
closing_commands = ["exit", "quit"]

unix_programs_dict = {
    "chrome": "/usr/bin/google-chrome",
    "google-chrome": "/usr/bin/google-chrome",
    "brave": "/usr/bin/brave-browser",
    "vs code": "/usr/bin/code",
    "visual studio code": "/usr/bin/code",
    "phpstorm": "/snap/bin/phpstorm",
    "php storm": "/snap/bin/phpstorm"
}

windows_programs_dict = {
    "chrome": "chrome.exe",
    "brave": "brave.exe"
}

os_programs_dict = {
    "Windows": windows_programs_dict,
    "Linux": unix_programs_dict
}

engine = pyttsx3.init()


def SpeakText(command):
    engine.say(command)
    engine.runAndWait()


def get_programs_dict():
    whichOs = platform.system()
    return os_programs_dict.get(whichOs)


def checkForCommandInInput(inputFromUser):
    for comm in opening_commands:
        if comm in inputFromUser.lower():
            return True

    return False


def checkForAvailablePrograms(inputFromUser):
    programs = get_programs_dict()
    for prog in programs.keys():
        if prog in inputFromUser.lower():
            return programs[prog]

    return ""


def openSearch(q):
    wb.open_new_tab("https://google.com/search?q="+q)

def trigger_command(userinput):
    isOpenCommand = checkForCommandInInput(userinput)
    supportedProgram = checkForAvailablePrograms(userinput)

    if supportedProgram and isOpenCommand:
        print("Trying to start:" + supportedProgram)
        try:
            os.system(supportedProgram)
        except:
            print("OS Error occurred")
        finally:
            return True
    elif "exit" in userinput:
        print("Exiting program")
        return False
    else:
        openSearch(userinput)
        return True


print("Welcome to my Virtual Assistant")
# loops until user specify to quit
print("I'm listening, what you want to do?")

microphone = sr.Microphone()
duration = 5

with microphone as source:
    r.adjust_for_ambient_noise(source)

while True:
    try:
        # use the microphone as source for input.
        with microphone as source:
            print("Listening...")
            audio_data = r.record(source, duration=duration)
            print("Recognizing...")
            text = r.recognize_google(audio_data)
            print("You said + " + text)
            SpeakText(text)
            res = trigger_command(text)

            if not res:
                break
    except sr.UnknownValueError:
        print("No voice detected")

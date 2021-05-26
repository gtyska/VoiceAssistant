import speech_recognition as sr
import pyttsx3
import errors as err

recognizer = sr.Recognizer()
speaking_engine = pyttsx3.init()

# English voice below is setted only if it is downloaded (otherwise - the default voice is used):
english_voice_ID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"

try:
    speaking_engine.setProperty("voice", english_voice_ID)
except Exception:
    pass


def saveName(name):
    file = open('name.txt', "w")
    file.write(name)
    file.close()


def getSavedName():
    name = ""
    try:
        file = open('name.txt')
        for line in file:
            name = line
            break
    except Exception:
        name = ""
    return name


def intro():
    name = getSavedName()
    knows_name = intro_speak_knows_name(name)
    if not knows_name:
        error, name = listen()
        if error != 0:
            speak(name)
            speak("Please say your name one more time.")
            error, name = listen()
            if error != 0:
                speak("Please, check your microphone and remember that too much noise around makes it impossible for me to recognize your voice.")
                return err.error_recognition

        name = name.split(" ")[0]
        saveName(name)
        speak("Hello {}, what can I do for you?".format(name))
    return 0


def get_message():
    error, message = listen()
    return error, message


def intro_speak_knows_name(name):
    knows_name = False
    if name != "":
        knows_name = True
        msg = "Hello, what can I do for you" + name + "?"
    else:
        msg = "Hello, I am your voice assistant. My name is Clevera. What is your name?"
    speak(msg)
    return knows_name


def speak(message):
    speaking_engine.say(message)
    speaking_engine.runAndWait()


def listen():
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            message = recognizer.recognize_google(audio)
        except Exception:
            return err.error_recognition, "Sorry, I couldn't recognize your voice"
    return 0, message


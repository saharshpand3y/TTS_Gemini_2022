import speech_recognition as sr
from gtts import gTTS
import os
import requests
from pydub import AudioSegment
from pydub.playback import play
from pydub.utils import mediainfo
import asyncio
import sys

sys.stderr = open('/dev/null', 'w')
def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        print("Recognizing...")
        try:
            text = recognizer.recognize_google(audio)
            print("You said:", text)
        except sr.UnknownValueError:
            print("Could not understand audio")
            text = 'Could not understand audio'
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
            text = 'Could not request results'
    return text

def generate_response(text):

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-lite:generateContent?key=" #API_KEY
    payload = {
        "contents": [{
            "parts": [{
                "text": text
            }]
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers).json()

    return response['candidates'][0]['content']['parts'][0]['text']

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    # os.system("mpg123 response.mp3")

def play_audio(file_path):
    audio_info = mediainfo(file_path)
    format_name = audio_info.get("format", "mp3")
    sound = AudioSegment.from_file(file_path, format=format_name)
    play(sound)

if __name__ == "__main__":
    while True:
        try:
            input_text = recognize_speech()
            if input_text:
                response_text = generate_response(input_text)
                print("Response:", response_text)
                speak_text(response_text)
                play_audio('response.mp3')
                os.system('rm response.mp3')
                if input_text == 'exit':
                    exit(0)
        except KeyboardInterrupt:
            print("Exiting...")

from flask import Flask, request, jsonify, render_template
import speech_recognition as sr
import webbrowser
import datetime
import requests
import os
import threading
from mistralai import Mistral
import edge_tts
import asyncio
import pygame

app = Flask(__name__)
app.secret_key = 'elnur'

mistral_api_key = 'UC3u1sHrt1mQxELxkx5s3wNUbMk7ouQO'

pygame.mixer.init()

VOICE_MALE = "en-US-GuyNeural"
VOICE_FEMALE = "en-US-AriaNeural"

VOICE_GENDER = VOICE_FEMALE  # DEFAULT VOICE
VOICE_SPEED = "+0%"
VOICE_TURKISH = 'tr-TR-AhmetNeural'


def run_mistral(prompt):
    model = "mistral-small-latest"

    client = Mistral(api_key=mistral_api_key)

    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            },
        ]
    )

    return chat_response.choices[0].message.content


def extract_city_name(query):
    keywords = ["in", "at", "for"]
    query_parts = query.lower().split()
    for keyword in keywords:
        if keyword in query_parts:
            city_index = query_parts.index(keyword) + 1
            if city_index < len(query_parts):
                return query_parts[city_index]
    return None


async def speak(text):
    communicate = edge_tts.Communicate(text, VOICE_GENDER, rate=VOICE_SPEED)

    await communicate.save("output.mp3")

    pygame.mixer.music.load("output.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.music.unload()
    os.remove("output.mp3")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stop-talking', methods=['POST'])
def stop_talking():
    pygame.mixer.music.stop()
    return jsonify({'status': 'success'})


@app.route('/get-information', methods=['POST'])
def get_information():
    pygame.mixer.music.stop()
    if request.method == 'POST':
        data = request.get_json()
        query = data['query'].lower()

        try:
            if 'hello' in query:
                threading.Thread(target=lambda: asyncio.run(
                    speak("Hello, Good Day, Welcome to Voice Assistant, How can i help you?"))).start()
            elif 'open google' in query:
                if 'search' in query:
                    search_query = query.split(
                        'open google and search')[-1].strip()
                    search_google(search_query)
                    speak(f"Searching Google for {search_query}")
                else:
                    webbrowser.open("https://www.google.com/")
                    threading.Thread(target=lambda: asyncio.run(
                        speak("Opening Google..."))).start()

            elif 'open youtube' in query:
                if 'search' in query:
                    search_query = query.split(
                        'open youtube and search')[-1].strip()
                    search_youtube(search_query)
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Searching on youtube for {search_query}"))).start()
                else:
                    webbrowser.open("https://www.youtube.com/")
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Opening Youtube..."))).start()

            elif 'switch language' in query:
                global VOICE_GENDER
                if 'english' in query:
                    VOICE_GENDER = VOICE_FEMALE
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Language is Switched to English."))).start()
                elif 'turkish' in query:
                    VOICE_GENDER = VOICE_TURKISH
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Dil Türkçe olarak seçildi."))).start()
                    return jsonify({'status': 'success', 'language': 'tr-TR'})

            elif 'open google maps' in query:
                if 'search' in query:
                    search_query = query.split(
                        'open google maps and search')[-1].strip()
                    search_google_maps(search_query)
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Searching on google maps for {search_query}"))).start()
                else:
                    webbrowser.open("https://www.google.com/maps/")
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Opening google maps..."))).start()

            elif 'time' in query:
                current_time = datetime.datetime.now().strftime("%I:%M %p")
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"The current time is {current_time}"))).start()

                return jsonify({'status': 'success', 'response': current_time})

            elif 'date' in query:
                current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"Today is {current_date}"))).start()
                return jsonify({'status': 'success', 'response': current_date})

            elif 'speed' in query:
                global VOICE_SPEED
                speed = 0
                if 'normal' in query:
                    speed = 0
                else:
                    try:
                        speed = int(query.split()[-1])
                    except ValueError:
                        print(
                            "Invalid speed value. Please provide a valid speed value.")

                VOICE_SPEED = f"+{speed}%"
                if speed == 0:
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Voice speed is set to normal."))).start()
                else:
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Voice speed is increased {speed} percent"))).start()
            elif 'change voice' in query:
                # global VOICE_GENDER
                if 'female' in query:
                    VOICE_GENDER = VOICE_FEMALE
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Voice is changed to Female."))).start()
                elif 'male' in query:
                    VOICE_GENDER = VOICE_MALE
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Voice is changed to Male."))).start()

                else:
                    threading.Thread(target=lambda: asyncio.run(
                        speak(f"Invalid voice option. Please choose a valid voice."))).start()
            elif 'weather' in query:
                city = extract_city_name(query)
                weather_info = get_weather_info(city)
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"{weather_info}."))).start()
                return jsonify({'status': 'success', 'response': weather_info})

            elif 'joke' in query:
                joke = get_joke()
                threading.Thread(target=lambda: asyncio.run(
                    speak(joke))).start()
                return jsonify({'status': 'success', 'response': joke})

            elif 'open google and search' in query:
                search_query = query.split(
                    'open google and search')[-1].strip()
                search_google(search_query)
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"Searching Google for {search_query}"))).start()

            elif 'open youtube and search' in query:
                search_query = query.split(
                    'open youtube and search')[-1].strip()
                search_youtube(search_query)
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"Searching YouTube for {search_query}"))).start()
            elif 'open google maps and search' in query:
                search_query = query.split(
                    'open google maps and search')[-1].strip()
                search_google_maps(search_query)
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"Playing Searching Google Maps for {search_query}"))).start()

            else:
                if VOICE_GENDER == VOICE_TURKISH:
                    query = query + " Answer it Only in TURKISH!"
                mistral_response = run_mistral(query)
                threading.Thread(target=lambda: asyncio.run(
                    speak(f"{mistral_response}"))).start()
                return jsonify({'status': 'success', 'response': mistral_response})

        except sr.UnknownValueError:
            threading.Thread(target=lambda: asyncio.run(
                speak("Sorry, I couldn't understand what you said."))).start()
        except sr.RequestError:
            threading.Thread(target=lambda: asyncio.run(
                speak("Sorry, there was an error processing your request."))).start()

        return jsonify({'status': 'success'})


def get_weather_info(city):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?unitGroup=metric&key=GHB9FABHY3VXLF5X3449TPHGG&contentType=json"
    response = requests.get(url)
    try:
        data = response.json()

        current_conditions = data.get('currentConditions', {})

        weather_info = {
            'temperature': current_conditions.get('temp', 'N/A'),
            'feels_like': current_conditions.get('feelslike', 'N/A'),
            'conditions': current_conditions.get('conditions', 'N/A'),
        }
        weather_summary = (f"Today's temperature is {weather_info['temperature']}°C. "
                           f"It feels like {weather_info['feels_like']}°C. "
                           f"The current conditions are {weather_info['conditions']}.")
        weather_summary = f"In {city}, " + weather_summary
        return weather_summary
    except Exception as e:
        return f"Sorry, I couldn't get the weather information for {city}"


def get_joke():
    joke_api_url = 'https://official-joke-api.appspot.com/random_joke'
    headers = {'Accept': 'application/json'}
    response = requests.get(joke_api_url, headers=headers)
    data = response.json()
    print(data)
    if 'setup' in data and 'punchline' in data:
        joke_text = data['setup'] + ' ' + data['punchline']
        return joke_text
    else:
        return 'Sorry, No joke available.'


def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)


def search_youtube(query):
    search_url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(search_url)


def search_google_maps(query):
    search_url = f"https://www.google.com/maps/search/{query}"
    webbrowser.open(search_url)


def get_user_response():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        user_response = recognizer.recognize_google(audio).lower()
        return user_response
    except sr.UnknownValueError:
        threading.Thread(target=lambda: asyncio.run(
            speak(f"Sorry, I couldn't understand that"))).start()
    except sr.RequestError as e:
        threading.Thread(target=lambda: asyncio.run(
            speak(f"Something wrong happened, sorry..."))).start()
    return ""


if __name__ == '__main__':
    app.run(debug=True)

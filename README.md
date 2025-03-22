# Voice_Assisstant
Voice Assistant Project Report
Project Overview
This project is about creating a voice-activated assistant, similar to Amazon Alexa or Google Assistant, but
using Mistral AI's large language model (LLM) for understanding and responding to user commands. The
assistant can understand spoken commands, perform various tasks, and engage in conversations in multiple
languages.
Project Goals
The main goals of this project are:
1. Develop a Functional Voice-Activated Assistant: Create a system that can accurately transcribe
spoken language, understand user intent, and respond appropriately.
2. Leverage Mistral AI's LLM: Showcase the capabilities of Mistral AI's language model for natural
language processing (NLP) tasks.
3. Support Multiple Languages: Make the assistant capable of understanding and responding in both
English and Turkish.
4. Provide a Seamless User Experience: Ensure the interaction with the assistant is intuitive and natural,
mimicking human conversation.
5. Demonstrate Integration with External Services: Show the assistant's ability to interact with other
web services like search engines (Google, YouTube), map services (Google Maps), and APIs for weather
information and jokes.
Implementation Details
The voice-activated assistant is built using Python libraries and web technologies, managed through a Flask
web application. The workflow can be divided into several stages:
1. Speech Recognition
Library: speech_recognition (which uses Google's Speech Recognition API)
Functionality:
The user starts the interaction by clicking a "Start Listening" button on the web interface.
The system captures audio input from the user's microphone.
The speech_recognition library converts the audio into text, transcribing the spoken command.
The recognized text (query) is sent to the backend for processing.
2. Natural Language Understanding and Response Generation
Library: Mistral AI (specifically, the mistral-small-latest model)
Functionality:
The transcribed text is sent as a prompt to Mistral AI's LLM.
For multilingual support, if the language is set to Turkish, the prompt is appended with "Answer it Only
in TURKISH!".
Mistral AI analyzes the query, understands the user's intent, and generates a contextually appropriate
response.
The generated response is returned to the Flask application.
3. Task Execution and External Service Integration
Libraries: webbrowser, requests, datetime
Functionality:
The application parses the user's query to identify specific commands or requests.
Based on the identified intent, the system performs actions such as:
Opening Websites: webbrowser.open() is used to open specific URLs in the user's default
browser (e.g., Google, YouTube, Google Maps).
Searching: For search queries, the URL is constructed with the query parameters and opened
using webbrowser.
Retrieving Information:
Time/Date: The datetime library is used to get the current time and date, which is then
formatted and spoken to the user.
Weather: The requests library is used to fetch weather data from the Visual Crossing
Weather API. The response is parsed, and a summary is generated and spoken.
Jokes: The requests library is used to fetch a random joke from the Official Joke API. The
joke is then spoken to the user.
Customizing Voice Settings: The voice speed and gender are adjusted by modifying global
variables (VOICE_SPEED, VOICE_GENDER) that are used by the text-to-speech engine.
4. Text-to-Speech
Library: edge_tts (for text-to-speech) and pygame (for audio playback)
Functionality:
The generated response (either from Mistral AI or from internal logic) is passed to the edge_tts library.
edge_tts converts the text into audio, utilizing the specified voice (VOICE_GENDER) and speed
(VOICE_SPEED).
The audio is saved as a temporary "output.mp3" file.
pygame is used to play the audio file through the user's speakers.
The temporary audio file is deleted after playback.
There is a stop button to stop the current voice playing.
5. Web Interface
Libraries/Frameworks: Flask, HTML, CSS, JavaScript, jQuery
Functionality:
The Flask framework handles the routing and backend logic of the web application.
The user interface is built using HTML, CSS, and JavaScript.
jQuery is used for DOM manipulation and AJAX calls to communicate with the Flask backend.
The interface provides a "Start Listening" button, a visual indicator when the system is listening, a
waiting icon during processing, and an output area to display the transcribed command and the
assistant's response.
AJAX is used to send the transcribed text to the backend and receive the response, updating the
interface dynamically.
Used Libraries and Technologies
Python: The primary programming language for the backend logic.
Flask: A lightweight web framework for creating the web application.
speech_recognition: For speech-to-text conversion.
Mistral AI: For natural language understanding and response generation.
edge_tts: For text-to-speech conversion.
pygame: For audio playback.
webbrowser: For opening websites and handling web searches.
requests: For making HTTP requests to external APIs (weather, jokes).
datetime: For handling date and time information.
HTML, CSS, JavaScript: For creating the user interface.
jQuery: For DOM manipulation and AJAX calls.
Visual Crossing Weather API: For retrieving weather information.
Official Joke API: For retrieving random jokes.
Project Structure and Workflow
The following diagram illustrates the project's structure and the flow of information between its components:
voice_assistant/
│
├── app.py
├── requirements.txt
├── templates/
│ └── index.html
└── static/
└── images/
└── waiting.gif
+---------------------+
| User Interface |
| (index.html) |
+---------+-----------+
|
v
+---------+-----------+
| Flask Routes |
| (/get-information) |
+---------+-----------+
|
v
+---------+-----------+
| Query Processing |
| (get_information) |
+---------+-----------+
|
v
+---------+-----------+
| Action Handlers |
| (e.g., open Google,|
| switch language, |
| get weather info) |
+---------+-----------+
|
v
+---------+-----------+
| Speech Synthesis |
| (speak function) |
+---------+-----------+
|
v
+---------+-----------+
| External APIs |
| (Mistral, Weather, |
| Joke) |
+---------+-----------+
|
v
+---------+-----------+
| Web Browser Actions|
| (webbrowser module)|
+---------+-----------+
|
v
+---------+-----------+
| Speech Recognition |
| (get_user_response)|
+---------------------+
User Interface (index.html):
The user interacts with the voice assistant through the web interface.
User queries are captured and sent to the Flask backend.
Flask Routes (/get-information):
The /get-information route receives the user query via a POST request.
The query is processed to determine the appropriate action.
Query Processing (get_information):
The get_information function analyzes the query and decides the action to take.
Depending on the query, it calls the relevant action handler.
Action Handlers:
Open Google/YouTube/Maps:
if 'open google' in query.lower():
webbrowser.open('https://www.google.com')
elif 'open youtube' in query.lower():
webbrowser.open('https://www.youtube.com')
elif 'open maps' in query.lower():
webbrowser.open('https://maps.google.com')
Switch Language:
if 'switch to turkish' in query.lower():
recognition.lang = 'tr-TR'
VOICE_GENDER = 'VOICE_TURKISH'
elif 'switch to english' in query.lower():
recognition.lang = 'en-US'
VOICE_GENDER = 'VOICE_FEMALE'
Get Weather Info:
if 'weather' in query.lower():
city = query.split('in')[-1].strip()
weather_response =
requests.get(f'https://api.visualcrossing.com/weather?city={city}')
weather_data = weather_response.json()
response = f"The weather in {city} is {weather_data['description']}
with a temperature of {weather_data['temperature']} degrees."
Get Joke:
if 'tell me a joke' in query.lower():
joke_response = requests.get('https://official-jokeapi.
appspot.com/random_joke')
joke_data = joke_response.json()
response = f"Here's a joke: {joke_data['setup']} ...
{joke_data['punchline']}"
General Queries:
if 'who is' in query.lower() or 'what is' in query.lower():
response = mistral.generate(query)
Speech Synthesis (speak function):
Converts the response text to speech using Edge TTS.
Plays the speech using Pygame's mixer.
External APIs:
Mistral API: Provides responses for general queries.
Weather API: Fetches weather information.
Joke API: Fetches jokes.
Web Browser Actions (webbrowser module):
Opens Google, YouTube, or Google Maps based on the query.
Speech Recognition (get_user_response):
Captures user voice input using the SpeechRecognition library.
Converts the voice input to text for processing.
Multilingual Support
The assistant supports both English and Turkish. The language selection is handled by modifying the
recognition.lang parameter in the JavaScript code and by appending "Answer it Only in TURKISH!" to the
prompt sent to Mistral AI when the Turkish language is selected. The VOICE_GENDER variable is also updated
to use the appropriate voice for each language (VOICE_FEMALE for English and VOICE_TURKISH for Turkish).
Customization
The assistant's voice can be customized in terms of:
Gender: The VOICE_GENDER variable can be set to either VOICE_MALE or VOICE_FEMALE (or
VOICE_TURKISH for Turkish) to change the voice used for text-to-speech.
Speed: The VOICE_SPEED variable can be adjusted to control the speaking rate. The user can provide
commands like "increase speed by 20" or "set speed to normal" to modify this setting.
Error Handling
The code includes basic error handling for:
Speech Recognition Errors: If the speech recognition engine fails to understand the user's input or
encounters a request error, it displays an appropriate message to the user.
API Errors: If there's an issue fetching data from external APIs (e.g., weather or jokes), the assistant
informs the user that it couldn't retrieve the requested information.
Microphone Access: If the browser cannot access the user's microphone, an alert is displayed.
Handling Commands
The assistant handles commands by parsing the user's query to identify specific intents and executing
corresponding actions. For example:
Opening Websites: If the query includes a request to open a website, the assistant uses
webbrowser.open() to navigate to the specified URL.
Searching Information: For search queries, the assistant constructs a search URL and opens it in the
default browser.
Retrieving Data: For requests like weather or jokes, the assistant makes HTTP requests to the relevant
APIs, processes the response, and provides the information to the user.
Custom Commands: The assistant can also handle custom commands like adjusting voice settings or
providing the current time and date.
Examples from app.py
Here are some examples from the app.py file, explaining each part:
1. Importing Libraries
from flask import Flask, request, jsonify
import speech_recognition as sr
import mistral
import edge_tts
import pygame
import webbrowser
import requests
import datetime
Explanation: This section imports the necessary libraries for the application, including Flask for the web
framework, speech recognition, Mistral AI, text-to-speech, and other utilities.
2. Initializing Flask App
app = Flask(__name__)
Explanation: This line initializes the Flask application.
3. Speech Recognition Route
@app.route('/recognize', methods=['POST'])
def recognize_speech():
recognizer = sr.Recognizer()
audio_file = request.files['audio']
with sr.AudioFile(audio_file) as source:
audio = recognizer.record(source)
try:
text = recognizer.recognize_google(audio)
return jsonify({'text': text})
except sr.UnknownValueError:
return jsonify({'error': 'Could not understand audio'})
except sr.RequestError:
return jsonify({'error': 'Could not request results from Google Speech
Recognition service'})
Explanation: This route handles speech recognition. It receives an audio file, processes it using the
speech_recognition library, and returns the transcribed text.
4. Generating Response with Mistral AI
@app.route('/generate', methods=['POST'])
def generate_response():
data = request.json
prompt = data['prompt']
response = mistral.generate(prompt)
return jsonify({'response': response})
Explanation: This route sends the transcribed text to Mistral AI's LLM and returns the generated response.
5. Text-to-Speech Conversion
@app.route('/speak', methods=['POST'])
def speak_text():
data = request.json
text = data['text']
tts = edge_tts.TTS()
tts.speak(text, 'output.mp3')
pygame.mixer.init()
pygame.mixer.music.load('output.mp3')
pygame.mixer.music.play()
return jsonify({'status': 'playing'})
Explanation: This route converts the generated text response to speech using edge_tts and plays it using
pygame.
6. Running the Flask App
if __name__ == '__main__':
app.run(debug=True)
Explanation: This line runs the Flask application in debug mode.
Examples from index.html
Here are some examples from the index.html file, explaining each part:
1. HTML Structure
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Voice Assistant</title>
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div id="app">
<button id="start-listening">Start Listening</button>
<div id="status">Status: Idle</div>
<div id="output"></div>
</div>
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<script src="app.js"></script>
</body>
</html>
Explanation: This section defines the basic HTML structure, including a button to start listening, a status
indicator, and an output area. It also includes links to the CSS file and JavaScript file.
2. JavaScript for Handling User Interaction
$(document).ready(function() {
$('#start-listening').click(function() {
$('#status').text('Status: Listening...');
// Code to capture audio and send it to the backend
});
});
Explanation: This script handles the click event for the "Start Listening" button, updating the status indicator
and initiating the process to capture audio and send it to the backend.
3. AJAX Call to Flask Backend
function sendAudioToBackend(audioBlob) {
var formData = new FormData();
formData.append('audio', audioBlob);
$.ajax({
url: '/recognize',
type: 'POST',
data: formData,
processData: false,
contentType: false,
success: function(response) {
$('#output').text('You said: ' + response.text);
generateResponse(response.text);
},
error: function() {
$('#status').text('Status: Error');
}
});
}
Explanation: This function sends the captured audio to the Flask backend using an AJAX call. It updates the
output area with the transcribed text and calls another function to generate a response.
4. Generating Response
function generateResponse(prompt) {
$.ajax({
url: '/generate',
type: 'POST',
contentType: 'application/json',
data: JSON.stringify({ prompt: prompt }),
success: function(response) {
$('#output').append('<br>Assistant: ' + response.response);
speakText(response.response);
},
error: function() {
$('#status').text('Status: Error');
}
});
}
Explanation: This function sends the transcribed text to the Flask backend to generate a response using
Mistral AI. It updates the output area with the assistant's response and calls another function to convert the
response to speech.
5. Text-to-Speech
function speakText(text) {
$.ajax({
url: '/speak',
type: 'POST',
contentType: 'application/json',
data: JSON.stringify({ text: text }),
success: function() {
$('#status').text('Status: Speaking');
},
error: function() {
$('#status').text('Status: Error');
}
});
}
Explanation: This function sends the generated response text to the Flask backend to convert it to speech. It
updates the status indicator to show that the assistant is speaking.
Potential Improvements
1. More Robust Error Handling: Implement more comprehensive error handling to catch a wider range
of potential issues and provide more informative feedback to the user.
2. Contextual Awareness: Enhance the assistant's ability to maintain context across multiple turns of
conversation, allowing for more natural and engaging interactions.
3. Expanded Functionality: Integrate with more external services and APIs to provide a wider range of
capabilities (e.g., calendar integration, email, music playback, smart home control).
4. Personalization: Allow users to create profiles and customize the assistant's behavior, voice, and other
settings to their preferences.
5. Advanced NLP Techniques: Explore more advanced NLP techniques, such as named entity recognition
and sentiment analysis, to further improve the assistant's understanding of user input.
6. Offline Capabilities: Investigate options for providing some level of offline functionality, perhaps by
utilizing on-device speech recognition and a smaller, localized language model.
7. Improved UI/UX: Refine the user interface and user experience to make the interaction even more
intuitive and seamless.
8. Security: Implement appropriate security measures to protect user data and privacy.
Conclusion
This project successfully demonstrates the development of a functional voice-activated assistant powered by
Mistral AI's LLM. The assistant showcases the potential of combining advanced NLP with web technologies to
create engaging and useful applications. While there's room for further development and improvement, the
current implementation provides a solid foundation for building a more sophisticated and feature-rich voice
assistant. The project highlights the power and versatility of Mistral AI's language models, particularly in the
realm of natural language understanding and generation, paving the way for more advanced and intuitive
human-computer interactions in the future.

import google.generativeai as genai
import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3


# Load the Google API key from environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

# Configure GenAI with the Google API key
genai.configure(api_key=google_api_key)

# Load personality from file
personality = "personality.txt"
with open(personality, "r") as file:
    mode = file.read()

# Define initial messages aand setting the personality of the chatbot
messages = [
    {"role": "system", "content": mode}  # Personality message
]

#this will get all the voices in the system and initialise the text speech
engine=pyttsx3.init()
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id) #0 for male,1 for female

#setting the microphone
r=sr.Recognizer()
mic=sr.Microphone(device_index=0)
r.dynamic_energy_threshold=False
r.energy_threshold = 400

while True:
  with mic as source:
     print("\nListening....")
     r.adjust_for_ambient_noise(source,duration=0.5)  #this will listen to audio
     audio = r.listen(source)                          #the audio will be astored in audio 
     try:
            # if usewhisper:
            #     user_input = whisper(audio)
            # else:
            user_input = r.recognize_google(audio)         #this will check in recognize_google if it has spoken any word then recognize it and store it in user input
     except:
            continue


# Add user input to messages
  messages.append({"role": "user", "content": user_input})

# Initialize the Gemini-Pro model
  model = genai.GenerativeModel('gemini-pro')

# Generate response
  response = model.generate_content(user_input)

# Access text content from the response parts
  response_text = response.parts[0].text

# Add response to messages
  messages.append({"role": "assistant", "content": response_text})

# Print the response
  print(f"\n{response_text}\n")

  engine.say(f'{response_text}')
  engine.runAndWait()

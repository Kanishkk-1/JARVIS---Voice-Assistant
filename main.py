import os
import speech_recognition as sr
import win32com.client
import datetime
import requests
import json
from config import apikey 

speaker = win32com.client.Dispatch("SAPI.spVoice")
chatStr = ""
def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Boss: {query}\nJARVIS: "
    
    try:
        # Updated model name
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={apikey}'
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'contents': [{
                'parts': [{
                    'text': f"You are JARVIS, an AI assistant. Respond to: {query}"
                }]
            }]
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['candidates'][0]['content']['parts'][0]['text']
            say(reply)
            chatStr += f"{reply}\n"
            return reply
        else:
            print(f"Gemini API error: {response.status_code} - {response.text}")
            say("Sorry, I'm having trouble processing that request")
            return "Error occurred"
            
    except Exception as e:
        print(f"Gemini API error: {e}")
        say("Sorry, I'm having trouble processing that request")
        return "Error occurred"

def ai(prompt):
    try:
        # Updated model name
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={apikey}'
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'contents': [{
                'parts': [{
                    'text': prompt
                }]
            }]
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            reply = result['candidates'][0]['content']['parts'][0]['text']
            
            if not os.path.exists("Gemini"):
                os.mkdir("Gemini")
            
            filename = prompt.replace("Hey Jarvis", "").strip()[:50]
            with open(f"Gemini/{filename}.txt", "w") as f:
                f.write(f"Response to: {prompt}\n-----------------------\n\n{reply}")
                
            say(reply)
        else:
            print(f"Gemini API error: {response.status_code} - {response.text}")
            say("Sorry, I'm having trouble with that request")
            
    except Exception as e:
        print(f"Gemini API error: {e}")
        say("Sorry, I'm having trouble with that request")

# Rest of your code remains the same
def say(text):
    speaker.Speak(text)

def take_voice():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source, timeout=5)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            return "Sorry, I don't understand what you say?"
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return "Sorry, speech recognition service is unavailable"
        except Exception as e:
            print(f"Error: {e}")
            return "Sorry, I don't understand what you say?"

if __name__ == '__main__':
    print('Starting JARVIS...')
    say("Hello Kanishk, I am JARVIS. How may I help you today?")
    
    while True:
        try:
            text = take_voice()
            if text == "Sorry, I don't understand what you say?":
                continue
                
            print("You said:", text)
            
            if "the time" in text.lower():
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")
                say(f"Sir, the current time is {strfTime}")
            elif "thank you" in text.lower():
                say("Sir, it was my duty")
            elif "hey jarvis" in text.lower():
                ai(prompt=text)
            elif "jarvis quit" in text.lower():
                say("Goodbye sir!")
                exit()
            elif "reset chat" in text.lower():
                chatStr = ""
                say("Chat history reset")
            else:
                print("Chatting...")
                chat(text)
                
        except KeyboardInterrupt:
            say("Goodbye sir!")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            say("Sorry, something went wrong")


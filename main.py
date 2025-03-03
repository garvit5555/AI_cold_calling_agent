import streamlit as st
import speech_recognition as sr
import re
import threading
from gtts import gTTS
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.playback import play
from datetime import datetime
from demo_scheduling import demo_scheduling_tool
from candidate_screening import candidate_screening_tool
from payment_followup import call_all_customers
import os
from deep_translator import GoogleTranslator
import pygame


# Configure the page
st.set_page_config(page_title="AI Voice Call Agent", layout="centered")
st.title("🤖 AI Voice Call Agent")

# Initialize translator for Hinglish to Hindi conversion
translator = GoogleTranslator(source="auto", target="hi")

# Function to recognize speech from microphone
def recognize_speech():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        st.markdown('<div class="listening-indicator">🎤 Listening... Speak now!</div>', unsafe_allow_html=True)
        
        # Reduce background noise dynamically
        recognizer.adjust_for_ambient_noise(source, duration=1)  

        try:
            audio = recognizer.listen(source, timeout=5)  # Wait for speech with timeout
            text = recognizer.recognize_google(audio, language="en-IN")  # Recognize speech
            return text
        except sr.WaitTimeoutError:
            return "No speech detected. Please try again."
        except sr.UnknownValueError:
            return "Sorry, mujhe samajh nahi aaya."
        except sr.RequestError:
            return "Speech Recognition service filhaal uplabdh nahi hai."
        except Exception as e:
            return f"Error: {e}"

# Function to clean text (removes special characters)
def clean_text(text):
    text = re.sub(r'[""":,\'!@#$%^&*()_+=\[\]{}<>?/|\\]', '', text)  # Remove unwanted symbols
    text = text.replace('\n', ' ')  # Replace newlines with space
    return text

# Function to Convert Text to Hindi Speech


def speak(text):
    try:
        # Translate text to Hindi
        translator = GoogleTranslator(source="auto", target="hi")
        hindi_text = translator.translate(text)

        # Generate speech and save to a temporary file
        temp_file = "temp_audio.mp3"
        tts = gTTS(text=hindi_text, lang="hi")
        tts.save(temp_file)

        # Initialize pygame mixer
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        # Wait until playback is finished
        while pygame.mixer.music.get_busy():
            continue  # Keeps script alive while audio plays

        # Clean up
        pygame.mixer.quit()
        os.remove(temp_file)

    except Exception as e:
        print(f"Error in speech synthesis: {e}")

# Run in a separate thread for smooth playback
def speak_threaded(text):
    threading.Thread(target=speak, args=(text,), daemon=True).start()




# ✅ **Initialize Session State**
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "candidate_role" not in st.session_state:
    st.session_state.candidate_role = None
if "last_scenario" not in st.session_state:
    st.session_state.last_scenario = None
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# ✅ **Scenario Selection**
st.subheader("Select a Scenario to Begin")
scenario = st.selectbox("Select Scenario", ["Select a scenario", "demo_scheduling", "candidate_screening", "payment_followup"], index=0)

if scenario == "Select a scenario":
    st.warning("Please select a scenario to continue.")
    st.stop()

# ✅ **Set Initial Message When Scenario Changes**
initial_messages = {
    "demo_scheduling": "ERP software aapke business ko streamline karne me madad karega. Kya main usko dikhaane ke liye ek demo schedule kar sakta hoon?",
    "candidate_screening": "Namaste! Main XYZ ka interviewer hoon. Aap kis job role ke liye apply kar rahe hain?",
}

if scenario != st.session_state.last_scenario:
    st.session_state.conversation = []  # ✅ Reset conversation
    
    if scenario in initial_messages:
        initial_message = initial_messages[scenario]
        st.session_state.conversation.append(("AI", initial_message, datetime.now().strftime('%H:%M')))
        
        # Speak the initial message if using voice for this scenario
        if scenario in ["demo_scheduling", "candidate_screening"]:
            threading.Thread(target=speak, args=(initial_message,), daemon=True).start()
            
    st.session_state.last_scenario = scenario

# ✅ **Modern Chat UI Styling with Resizable Chat Bubbles**
st.markdown("""
    <style>
        .chat-container {
            max-width: 700px;
            margin: auto;
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .chat-bubble {
            border-radius: 20px;
            padding: 10px 15px;
            margin: 5px 0;
            display: inline-block;
            width: fit-content;
            max-width: 80%;
            min-width: 50px;
            resize: vertical; /* Allow resizing */
            overflow: auto;
        }
        .user {
            background-color: #dcf8c6;
            text-align: right;
            float: right;
            clear: both;
        }
        .ai {
            background-color: #f1f1f1;
            text-align: left;
            float: left;
            clear: both;
        }
        .timestamp {
            font-size: 12px;
            color: gray;
            margin-top: 5px;
            display: block;
        }
        .input-container {
            display: flex;
            align-items: center;
            margin-top: 20px;
        }
        .listening-indicator {
            color: #FF4B4B;
            font-weight: bold;
            margin-bottom: 10px;
            animation: blink 1s infinite;
        }
        @keyframes blink {
            0% {opacity: 1;}
            50% {opacity: 0.5;}
            100% {opacity: 1;}
        }
        .input-method-selector {
            display: flex;
            justify-content: center;
            margin-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# ✅ **Display Chat Messages**
chat_container = st.container()
with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for i, (role, msg, timestamp) in enumerate(st.session_state.conversation):
        bubble_class = "user" if role == "User" else "ai"
        st.markdown(f'<div class="chat-bubble {bubble_class}">{msg}<span class="timestamp">{timestamp}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ✅ **Typing Indicator**
if "typing" in st.session_state and st.session_state.typing:
    st.markdown("<div class='chat-bubble ai'>...</div>", unsafe_allow_html=True)

# Input Method Selection (Voice or Text)
st.markdown('<div class="input-method-selector">', unsafe_allow_html=True)
input_method = st.radio("Input Method", ["Text", "Voice"], horizontal=True)
st.markdown('</div>', unsafe_allow_html=True)

# Input Section
if input_method == "Voice" and scenario in ["demo_scheduling", "candidate_screening"]:
    if st.button("🎙 Speak"):
        user_input = recognize_speech()
        if user_input and not user_input.startswith("Error") and not user_input.startswith("No speech") and not user_input.startswith("Sorry"):
            st.session_state.user_input = user_input
            st.success(f"Recognized: {user_input}")
        else:
            st.warning(user_input)
else:
    st.session_state.user_input = st.text_input("📝 Your Response:", key="text_input")

# Process user input - both from voice and text
if st.button("Send") or ("user_input" in st.session_state and st.session_state.user_input):
    user_input = st.session_state.user_input
    st.session_state.user_input = ""  # Clear after using
    
    if scenario == "payment_followup":
        response = "📞 Calling customers for payment reminders..."
        st.session_state.conversation.append(("AI", response, datetime.now().strftime('%H:%M')))
        threading.Thread(target=call_all_customers, daemon=True).start()

    elif user_input:
        st.session_state.conversation.append(("User", user_input, datetime.now().strftime('%H:%M')))

        if scenario == "candidate_screening":
            if st.session_state.candidate_role is None:
                st.session_state.candidate_role = user_input.strip()
                response = f"Great! Aap {st.session_state.candidate_role} ke liye apply kar rahe hain. Ab main aapse kuch sawaal puchunga."
            else:
                response = candidate_screening_tool(user_input, st.session_state.candidate_role)

        elif scenario == "demo_scheduling":
            response = demo_scheduling_tool(user_input)
        else:
            response = "Scenario samajh nahi aaya."

        st.session_state.conversation.append(("AI", response, datetime.now().strftime('%H:%M')))
        
        # Speak the response if using voice for this scenario
        if scenario in ["demo_scheduling", "candidate_screening"] and input_method == "Voice":
            threading.Thread(target=speak, args=(response,), daemon=True).start()

    st.rerun()
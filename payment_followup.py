from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse, Gather
from flask import Flask, request
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

# 🔹 Google Gemini API Key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Google Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)
# 🔹 Twilio Credentials
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# 🔹 Manually Set Your Ngrok Public URL
NGROK_URL = os.getenv("NGROK_URL")

# Initialize Twilio Client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def generate_ai_response(user_message, amount):
    """Generates AI response using Google Gemini."""
    prompt = f"""
    You are a polite customer support assistant speaking Hinglish.
    A customer has a pending payment of {amount} rupees and received a call.
    The customer said: "{user_message}".
    Respond in Hinglish briefly.
    """
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompt)
    
    return response.text.strip() if response.text else "Mujhe samajh nahi aaya, kripya repeat karein."

# Load Payment Data
def load_payment_data(file_path="payment_data.json"):
    """Loads pending payment details from JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []

customers = load_payment_data()

# Flask App
app = Flask(__name__)

@app.route("/payment-reminder", methods=["GET", "POST"])  
def payment_reminder():
    """Handles the initial call and asks the customer for input."""
    name = request.args.get("name", "Customer")
    amount = request.args.get("amount", "0")
    phone_number = request.args.get("phone", "")

    response = VoiceResponse()

    message = f"Namaste {name}, aapka {amount} rupaye ka payment pending hai. Aap iske baare me baat karna chahenge?"
    response.say(message, voice="alice", language="hi-IN")

    gather = Gather(
        input="speech dtmf",
        timeout=5,
        num_digits=1,
        action="/process-response",  # ✅ Correct action endpoint
        method="POST"
    )
    response.append(gather)

    return str(response)


@app.route("/process-response", methods=["POST"])
def process_response():
    """Processes user response and generates AI response if needed."""
    user_response = request.form.get("SpeechResult", "").strip()
    # keypad_input = request.form.get("Digits", "").strip()
    amount = request.args.get("amount", "0")

    response = VoiceResponse()

    # if keypad_input:
    #     if keypad_input == "1":
    #         response.say(f"Aapne 1 dabaya. Aapke {amount} rupaye ka payment pending hai.", voice="alice", language="hi-IN")
    #     elif keypad_input == "2":
    #         response.say("Aapne 2 dabaya. Dhanyavaad, hum aapki madad karne ke liye yahan hain.", voice="alice", language="hi-IN")
    #     else:
    #         response.say("Kripya sahi vikalp chuniye. 1 ya 2 dabaiye.", voice="alice", language="hi-IN")

    if user_response:
        print(f"📢 User said: {user_response}")  # Debugging
        ai_reply = generate_ai_response(user_response, amount)
        print(f"🤖 AI Response: {ai_reply}")  # Debugging
        response.say(ai_reply, voice="alice", language="hi-IN")

    else:
        response.say("Mujhe koi response nahi mila. Kripya dobara try karein.", voice="alice", language="hi-IN")

    return str(response)


def make_payment_call(customer):
    """Calls a customer and directs them to the voice bot."""
    phone_number = customer["phone"]
    pending_amount = customer["payment_pending_amount"]
    
    twiml_url = f"{NGROK_URL}/payment-reminder?amount={pending_amount}&name={customer['name']}&phone={phone_number}"

    print(f"📞 Calling {phone_number} for payment reminder...")

    try:
        call = client.calls.create(
            to=phone_number,
            from_=TWILIO_PHONE_NUMBER,
            url=twiml_url,
            method="GET"
        )
        return call.sid
    except Exception as e:
        print(f"⚠ Error making call: {e}")
        return None


def call_all_customers():
    """Calls all users with pending payments."""
    for customer in customers:
        if customer["payment_pending_amount"] > 0:
            make_payment_call(customer)

if __name__ == "__main__":
    print("🚀 Starting Flask server...")
    # call_all_customers()  # ✅ Calls customers automatically when server starts
    app.run(host="0.0.0.0", port=5000, debug=True)

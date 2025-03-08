# AI Cold Calling Agent

## Overview

**AI Cold Calling Agent** is an AI-powered voice assistant designed to handle automated voice interactions efficiently. It facilitates candidate screening, demo scheduling, and payment follow-ups using AI-driven responses, speech recognition, and automated calling technology. The system integrates Google Calendar API, Twilio, and NLP-based speech recognition to ensure seamless and natural conversations.

## Features

### 1. Candidate Screening
- AI-driven **dynamic question generation** for interviews.
- Evaluates candidate responses based on AI-powered analysis (hidden from the user).
- Determines the **next question dynamically** based on candidate performance.
- Stores candidate responses for further evaluation.
- Uses **Speech Recognition System (Text-to-Speech & Speech-to-Text)** for seamless interaction.

### 2. Demo Scheduling
- Uses AI to **detect user availability**.
- Integrates with **Google Calendar API** to create and manage events.
- Stores event details in a structured **JSON file**.
- Provides instant scheduling confirmation via voice feedback.
- Uses **Speech Recognition System (Text-to-Speech & Speech-to-Text)** to facilitate voice-based interactions.

### 3. Payment Follow-ups
- **Automated calls** via Twilio to remind users of pending payments.
- AI-powered **natural voice responses** based on customer replies.
- Supports **speech recognition** for enhanced customer interaction.
- Logs all call responses and user interactions.

## Tech Stack

| Technology           | Purpose                        |
|---------------------|--------------------------------|
| **Python**          | Backend development            |
| **Flask**           | API handling for voice interactions |
| **Google Calendar API** | Scheduling and event management |
| **Twilio**          | Automated calling system      |
| **Google Generative AI (Gemini)** | AI-generated responses |
| **Speech Recognition (speech_recognition)** | User voice input processing |
| **Google Translate API (deep_translator)** | Language translation |
| **Streamlit**       | Web UI for easy interaction  |

## Installation

### Prerequisites
- Python **3.8+**
- Twilio Account for automated calling
- Google Cloud account for API access
- Ngrok Account for tunneling

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/garvit5555/AI_cold_calling_agent.git
   cd AI_cold_calling_agent
   ```
2. **Create a virtual environment:** (Optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Create a `.env` file in the root directory and add the following details:
     ```ini
     SERVICE_ACCOUNT_FILE=path/to/google-calendar-credentials.json
     SCOPES=https://www.googleapis.com/auth/calendar
     CALENDAR_ID=your-calendar-id
     EVENTS_FILE=events.json
     GOOGLE_API_KEY=your-gemini-api-key
     TWILIO_ACCOUNT_SID=your-twilio-account-sid
     TWILIO_AUTH_TOKEN=your-twilio-auth-token
     TWILIO_PHONE_NUMBER=your-twilio-phone-number
     NGROK_URL=your-ngrok-public-url
     ```

## Running the Application

There are different ways to run the code for different scenarios:

### **For Payment Follow-ups Scenario**
1. Open **three terminals**:
   - **First Terminal:** Run the Flask server:
     ```bash
     python payment_followup.py
     ```
   - **Second Terminal:** Run Ngrok on port 5000 (after authenticating with your Ngrok token):
     ```bash
     ngrok http 5000
     ```
   - **Third Terminal:** Run Streamlit UI:
     ```bash
     streamlit run main.py
     ```

### **For Candidate Screening and Demo Scheduling Scenario**
Simply run:
   ```bash
   streamlit run main.py
   ```

## Usage

### Candidate Screening
- Call the function `candidate_screening_tool(user_input, job_role)` to generate interview questions dynamically based on the user's responses.
- The AI evaluates the answers and proceeds with the next relevant question.

### Demo Scheduling
- Call `demo_scheduling_tool(user_input)` to check user availability and schedule a demo session.
- The event is created in Google Calendar, and the details are stored in `events_scheduled.json`.

### Payment Follow-ups
- Call `call_all_customers()` to initiate automated voice calls for pending payments to all the customers in the `payment_data.json`.
- AI interacts with the customer based on their responses and updates the status accordingly.

## API Endpoints

| Endpoint             | Method | Description                          |
|----------------------|--------|--------------------------------------|
| `/payment-reminder`  | `POST` | Initiates a payment reminder call   |
| `/process-response`  | `POST` | Processes user voice response and generates an AI reply |
| `/schedule-demo`     | `POST` | Schedules a demo session using AI  |

## Future Enhancements
**Unfinished Features:**

- **HubSpot API Integration** for retrieving customer details in the payment follow-up scenario.
- **Sentiment Analysis** for scoring responses in the interview process.
- **Email Notifications** for scheduled events in the demo scheduling scenario.
- **Conversation Memory** to ask interview questions based on previous responses.
- **Enhanced Customer Pitching** to encourage users to see the ERP demo.
- **CSV Data Storage** for storing scheduled event details.

## Challenges Faced

1. **Exhaustion of Gemini API Key** multiple times.
2. **Using Twilio** for making payment calls via Ngrok.
3. **Google Calendar API Implementation** to send scheduled event details to the user's calendar.
4. **Multiple Event Scheduling Issues** (as shown in the video).

## Video Demo
[Click here to watch the demo](https://drive.google.com/file/d/1LQSnOGbST5nspe6180t7rkQKB-TmpX5h/view?usp=sharing)

## Contributors
- **GARVIT (Project Lead)**

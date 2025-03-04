# AI_cold_calling_agent

## Overview

The **AI Voice Call Agent** is a multi-functional voice-based assistant designed for candidate screening, demo scheduling, and payment follow-ups. It leverages AI-driven responses, Google Calendar API, Twilio for voice calls, and NLP-based speech recognition.

## Features

### Candidate Screening
- AI-based dynamic question generation for interviews
- Evaluates candidate responses (hidden from the user)
- Returns the next question based on candidate performance

### Demo Scheduling
- Detects user availability via AI
- Creates events in Google Calendar
- Stores event details in a JSON file
- Provides scheduling confirmation

### Payment Follow-ups
- Uses Twilio for automated calls
- AI-powered voice responses based on customer replies
- Reminds users about pending payments
- Supports speech recognition for better interaction

## Tech Stack
- **Python**: Backend development
- **Flask**: API handling for voice interactions
- **Google Calendar API**: Scheduling and event management
- **Twilio**: Automated calling system
- **Google Generative AI (Gemini)**: AI-generated responses
- **Speech Recognition (`speech_recognition`)**: User voice input processing
- **Google Translate API (`deep_translator`)**: Language translation
- **Streamlit**: Web UI for easy interaction

## Installation

### Prerequisites
Ensure you have **Python 3.8+** installed.

### Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ai-voice-call-agent.git
   cd ai-voice-call-agent
   ```

2. Create a virtual environment (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory and add the following:
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

5. Run the application:
   ```sh
   python app.py
   ```

## Usage

- **Candidate Screening**: Calls `candidate_screening_tool(user_input, job_role)` to generate interview questions.
- **Demo Scheduling**: Calls `demo_scheduling_tool(user_input)` to schedule events.
- **Payment Follow-ups**: Calls `call_all_customers()` to start automated calls.

## API Endpoints

- `POST /payment-reminder` - Initiates a payment reminder call.
- `POST /process-response` - Processes user voice response and generates an AI reply.

## Future Enhancements

- Multi-language support for regional users
- Improved AI response personalization
- Integration with CRM tools for better customer management

## Contributors
- **GARVIT** (Project Lead)



import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

#  Retrieve variables from the environment
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Google API Key for Gemini
SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")  # Path to service account JSON
SCOPES = [os.getenv("SCOPES")]  # Google Calendar API scope

#  Set Environment Variable
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

#  Initialize LangChain LLM with Google Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", google_api_key=GOOGLE_API_KEY)

#  Google Calendar API Setup
creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
calendar_service = build("calendar", "v3", credentials=creds)

from dotenv import load_dotenv
import os
load_dotenv()

DATABASE_CONFIG = {
    "driver" : os.getenv("DATABASE_DRIVER"),
    "server" : os.getenv("DATABASE_SERVER"),
    "database" : os.getenv("DATABASE_NAME"),
    "trusted_connection" : os.getenv("DATABASE_TRUSTED_CONNECTION")
}

OPEN_API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("BASE_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
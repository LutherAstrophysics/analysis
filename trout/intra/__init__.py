import os

from dotenv import load_dotenv

load_dotenv()
DATA_DRIVE = os.getenv("DATA_DRIVE") or "/media/m23/S1/Python_Processed"

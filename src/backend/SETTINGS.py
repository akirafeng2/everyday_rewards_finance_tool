from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

FINANCE_FILE_PATH = Path(os.getenv("FINANCE_FILE_PATH"))
CONNECTION_DETAILS = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT")
}
ENV = os.getenv("ENV")
IP_ADDRESS = os.getenv("IP_ADDRESS")
SECRET_KEY = os.getenv("SECRET_KEY")

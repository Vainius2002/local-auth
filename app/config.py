import os
from dotenv import load_dotenv
load_dotenv()



DATABASE_URL = os.environ["DATABASE_URL"]
USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

ALLOWED_REDIRECT_URIS = os.environ["ALLOWED_REDIRECT_URIS"].split(",")

import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
TEST_MODE = os.getenv("TEST", False)

CHANNEL = -1001369053241

NYX = 703453307

api_id = int(os.getenv("ID"))
api_hash = os.getenv("HASH")

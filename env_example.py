import os
from dotenv import load_dotenv


load_dotenv("./.env")

key = "USERNAME1"
username = os.getenv(key, None)
username1 = os.environ.get(key, None)

print(username)
print(username1)

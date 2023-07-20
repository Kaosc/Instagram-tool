import os
import dotenv

dotenv.load_dotenv()

# add your username and password to .env file  
# or replace those with your username and password as string

# example:
# IG_USERNAME = "your_username"
# IG_PASSWORD = "your_password"

username = os.getenv("IG_USERNAME")
password = os.getenv("IG_PASSWORD")

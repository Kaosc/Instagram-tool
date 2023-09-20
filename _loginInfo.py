import os
import dotenv

dotenv.load_dotenv()

# add your username and password to .env file  
# or replace below variables with your username and password as string

# example .env file content:
   # IG_USERNAME = "your_username"
   # IG_PASSWORD = "your_password"

username = os.getenv("IG_USERNAME") # or replace with your username as string. eg: username = "your_username"
password = os.getenv("IG_PASSWORD") # or replace with your password as string. eg: password = "your_password"

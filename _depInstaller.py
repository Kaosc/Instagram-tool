import os

pips = ["selenium", "colored", "pillow", "python-dotenv", "instaloader"]

for pip in pips:
  os.system("pip install " + pip)  # Installs all the dependencies

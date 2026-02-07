import os

pips = ["selenium", "colored", "pillow", "python-dotenv", "instaloader"]

for pip in pips:
  os.system("py -m pip install " + pip)  # Installs all the dependencies

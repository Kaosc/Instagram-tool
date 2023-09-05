import os

pips = ["selenium", "colored", "pillow", "python-dotenv", "requests"]

for pip in pips:
  os.system("pip install " + pip)  # Installs all the dependencies

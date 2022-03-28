import os

import dotenv
from flask import Flask

# ---- Keys, Passwords, Etc. ---- #

dotenv.load_dotenv("C:/_CODING/Python/portfolio_passcodes.env")
app_SECRET_KEY = os.getenv("app_SECRET_KEY")

# ---- App Setup ---- #

app = Flask(__name__)

from application import routes

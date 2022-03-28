from flask import Flask
from flask_bootstrap import Bootstrap
import dotenv
import os

# ---- Keys, Passwords, Etc. ---- #

dotenv.load_dotenv("C:/_CODING/Python/portfolio_passcodes.env")
app_SECRET_KEY = os.getenv("app_SECRET_KEY")

# ---- App Setup ---- #

app = Flask(__name__)
Bootstrap(app)

from application import routes
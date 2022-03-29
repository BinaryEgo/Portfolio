import os

import dotenv
from flask import Flask
from flask_bootstrap import Bootstrap

# ---- Keys, Passwords, Etc. ---- #

dotenv.load_dotenv("C:/_CODING/Python/portfolio_passcodes.env")
app_SECRET_KEY = os.getenv("app_SECRET_KEY")

# ---- App Setup ---- #

app = Flask(__name__)
app.config['SECRET_KEY'] = app_SECRET_KEY
Bootstrap(app)


from application import routes




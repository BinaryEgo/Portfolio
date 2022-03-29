import os

import dotenv
from flask import Flask, render_template, request, flash, url_for, redirect, abort
from flask_bootstrap import Bootstrap
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from application.project_modules.forms import ContactForm, LoginForm, ResetPasswordForm, AddMessageForm, \
    EnterWebsiteForm, MovieLookupForm
from application.project_modules.email_manager import send_email, send_reset_pw_email, submit_tarot_message


# ---- Keys, Passwords, Etc. ---- #

# dotenv.load_dotenv("C:/_CODING/Python/portfolio_passcodes.env")
# app_SECRET_KEY = os.getenv("app_SECRET_KEY")
app_SECRET_KEY = os.environ.get("app_SECRET_KEY")

# ---- App Setup ---- #

app = Flask(__name__)
app.config['SECRET_KEY'] = app_SECRET_KEY
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home_page():
    logout_user()
    contact_form = ContactForm()

    if request.method == "POST":
        if contact_form.validate_on_submit():
            send_email(contact_form)
            return render_template('contact.html', form=contact_form, msg_sent=True)
        else:
            return render_template('contact.html', form=contact_form, msg_sent=False)

    return render_template('index.html', form=contact_form)


@app.route('/about')
def show_aboutme():
    logout_user()
    return render_template('aboutme.html')


# ---- Tarot Login Manager ---- #
login_manager = LoginManager()
login_manager.init_app(app)
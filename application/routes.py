import os
from functools import wraps

import requests.exceptions
import sqlalchemy.exc
from flask import render_template, request, flash, url_for, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from application import app
from application.project_modules.email_manager import send_email, send_reset_pw_email, submit_tarot_message
from application.project_modules.forms import ContactForm, LoginForm, ResetPasswordForm, AddMessageForm, \
    EnterWebsiteForm, MovieLookupForm
from application.project_modules.movies_interest_boxoffice import get_boxoffice_and_trends_table, \
    get_boxoffice_and_trends_figure, get_chart_from_database, get_movie_poster, get_movie_blurb, get_movie_date
from application.project_modules.robots_checker import get_url_name, create_robots_html
from application.project_modules.tarot_cards import TarotUser, CustomMessages, TarotManager, MessageGenerator, \
    tarot_messages, custom_messages, db


# ---- Main Web Pages ---- #

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


@app.route('/portfolio', methods=["GET", "POST"])
def show_portfolio():
    logout_user()
    return render_template('projects.html')


@app.route('/contact', methods=["GET", "POST"])
def show_contact():
    logout_user()
    contact_form = ContactForm()

    if request.method == "POST":
        if contact_form.validate_on_submit():
            send_email(contact_form)
            return render_template('contact.html', form=contact_form, msg_sent=True)
        else:
            return render_template('contact.html', form=contact_form, msg_sent=False)

    return render_template('contact.html', form=contact_form)


# -------- PORTFOLIO WEB PAGES -------- #

# -------- START TAROT -------- #
# ---- Tarot Card Manager ---- #
tarot_manager = TarotManager()

# ---- Tarot Message Generator ---- #
message_generator = MessageGenerator(messages=tarot_messages, user_messages=custom_messages)

# ---- Tarot Login Manager ---- #
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return TarotUser.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Sorry, you must login to continue.")
    return redirect(url_for('tarot_start'))


# -- Admin Only Decorator --#
def admin_only(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        try:
            if current_user.id != 1:
                return abort(403)
        except AttributeError:
            flash("Page is locked to Admin only. Please login.")
            redirect(url_for('tarot_start'))
        return function(*args, **kwargs)

    return decorated_function


# ---- Tarot Web Pages ---- #

# ---- Tarot Start ---- #
@app.route("/portfolio/tarot-reader/", methods=["GET", "POST"])
def tarot_start():
    login_form = LoginForm()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI", "sqlite:///tarot_user_base.db")

    if request.method == "POST":
        # ---- Send Register Form ---- #
        if request.form['action'] == "Register":
            return render_template('tarot_start.html',
                                   status="register",
                                   form=login_form)

        # ---- Register New User ---- #
        elif request.form['action'] == "Sign Me Up!":
            secure_password = generate_password_hash(
                password=request.form.get('password'),
                salt_length=12
            )
            new_user = TarotUser(
                username=request.form.get('username'),
                email=request.form.get('email'),
                password=secure_password,
            )

            if TarotUser.query.filter_by(username=new_user.username).first():
                flash("That username has already been claimed. Try another one!")
                return render_template('tarot_start.html',
                                       status="register",
                                       form=login_form)

            try:
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return render_template('tarot_start.html',
                                       status="login_success",
                                       username=request.form['username'].upper(),
                                       deal_cards=tarot_manager.deal_cards())

            except sqlalchemy.exc.IntegrityError:
                db.session.rollback()
                flash(f"{request.form.get('email')} already has an account. You may have entered the wrong username.")
                return render_template('tarot_start.html', status="try_again", form=login_form)

        # ---- Send Login Form --- #
        elif request.form['action'] == "Login":
            username = request.form.get('username')
            password = request.form.get('password')
            user = TarotUser.query.filter_by(username=username).first()

            try:
                if check_password_hash(user.password, password):
                    # ---- On Successful Login ---- #
                    login_user(user)
                    return render_template('tarot_start.html',
                                           status="login_success",
                                           username=username.upper(),
                                           deal_cards=tarot_manager.deal_cards())
                else:
                    flash('Password is incorrect, please try again.')
                    return render_template('tarot_start.html', status="try_again", form=login_form)

            except AttributeError:
                flash('We could not find you - please try entering your details again, or sign up!')
                return render_template('tarot_start.html', status="try_again", form=login_form)

    return render_template('tarot_start.html', form=login_form)


# ---- Tarot Second Round ---- #
@app.route('/portfolio/tarot-reader/next-round/')
@login_required
def next_round():
    first_num = request.args.get('first_num')
    return render_template('tarot_next_round.html',
                           first_num=first_num,
                           deal_cards=tarot_manager.deal_cards())


# ---- Tarot Last Round ---- #
@app.route('/portfolio/tarot-reader/last-round/')
@login_required
def last_round():
    first_num = int(request.args.get('first_num'))
    second_num = int(request.args.get('second_num'))
    return render_template('tarot_last_round.html',
                           first_num=first_num,
                           second_num=second_num,
                           running_sum=[first_num, second_num],
                           deal_cards=tarot_manager.deal_cards())


# ---- Tarot Display Message ---- #
@app.route('/portfolio/tarot-reader/your_message/')
@login_required
def tarot_end():
    first_num = int(request.args.get('first_num'))
    second_num = int(request.args.get('second_num'))
    third_num = int(request.args.get('third_num'))
    total = sum([first_num, second_num, third_num])

    message = message_generator.deliver_message(total)

    return render_template('tarot_end.html',
                           total=message,
                           deck=tarot_manager.tarot_deck,
                           selected_cards=[first_num, second_num, third_num])


# ---- Tarot Submit a New Message ---- #
@app.route('/portfolio/tarot-reader/add-your-own-message/', methods=["GET", "POST"])
@login_required
def add_message():
    add_message_form = AddMessageForm()

    if request.method == "POST":
        message = request.form['message']
        user = current_user.id
        link_to_accept = url_for("accept_new_message", message=message, user=user)

        submit_tarot_message(message, user, link_to_accept)
        flash("Thanks For Your Submission! We'll review it!", category='success')
        return redirect(url_for('add_message'))

    return render_template('tarot_add_message.html', form=add_message_form)


# ---- Tarot Accept A New Message ---- #
@app.route('/portfolio/tarot-reader/message_accepted/')
@admin_only
def accept_new_message():
    message = request.args.get('message')
    author_id = request.args.get('user')
    author = TarotUser.query.filter_by(id=author_id).first()
    new_message = CustomMessages(
        message=message,
        author=author
    )
    db.session.add(new_message)
    db.session.commit()
    flash("Message Accepted", category="success")
    return redirect(url_for('tarot_start'))


# ---- Tarot Logout ---- #
@app.route('/portfolio/tarot-reader/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('tarot_start'))


# ---- Tarot Reset Password Request ---- #
@app.route("/portfolio/tarot-reader/reset-password-request/", methods=["GET", "POST"])
def reset_password_request():
    email_form = LoginForm()

    if request.method == "POST":
        if request.form['action'] == "Send Reset Email":
            email = request.form['email']
            user = TarotUser.query.filter_by(email=email).first()
            request_by = user.username
            token = generate_password_hash(request_by)

            if TarotUser.query.filter_by(email=email).first() is None:
                flash("This email is not registered with us. Please make a new account.", category="fail")
                return redirect(url_for('reset_password_request'))

            else:
                flash("An e-mail was sent with a link to reset", category="success")
                send_reset_pw_email(email, request_by, url_for('reset_password_submit', token=token))
                return redirect(url_for('reset_password_request'))

    return render_template('tarot_reset_pw_request.html', form=email_form)


# ---- Tarot Reset Password Submit ---- #
@app.route("/portfolio/tarot-reader/reset-password/", methods=["GET", "POST"])
def reset_password_submit():
    reset_password = ResetPasswordForm()
    hashed_username = request.args.get('token')

    if request.method == "POST" and request.form['action'] == "Reset Password":
        # ---- Passwords Must Match ---- #
        if request.form['password'] != request.form['confirm_password']:
            flash("'Password' and 'Confirm Password' Must Match")
            return redirect(url_for('reset_password_submit', token=hashed_username))

        # ---- Check if username matches, if so Update Password ---- #
        if check_password_hash(hashed_username, request.form['username']):
            new_password = request.form['password']
            secure_new_password = generate_password_hash(new_password, salt_length=12)
            user_to_update = TarotUser.query.filter_by(username=request.form['username']).first()
            user_to_update.password = secure_new_password
            db.session.commit()

            flash("Password has been successfully changed", "success")
            return redirect(url_for('tarot_start'))

        # ---- If Username Does Not Exist ---- #
        else:
            flash("Username is incorrect. Please refer to the email that was sent to you.")
            return redirect(url_for('reset_password_submit', token=hashed_username))

    return render_template('tarot_reset_pw_submit.html', form=reset_password)


# -------- END TAROT -------- #


# -------- START ROBOTS.TXT CHECKER -------- #
@app.route('/portfolio/robots-txt-check/txt-file', methods=["GET", "POST"])
def show_robots_txt():
    logout_user()
    form = EnterWebsiteForm()

    if request.method == "POST":
        website = get_url_name(form['url'].data)
        try:
            robots_txt = create_robots_html(website)
        except requests.exceptions.InvalidURL:
            flash('Valid Urls must start with "https://" or "http://"')
            return redirect(url_for('show_robots_txt'))
        return render_template('robots_text.html',
                               website=website,
                               robots_txt=robots_txt,
                               )

    return render_template('robots_text.html', form=form)


# -------- END ROBOTS.TXT CHECKER -------- #


# -------- START DATA SCIENCE BOX OFFICE -------- #

# ---- Preloader ---- #
@app.route('/preload')
def page_preloader():
    return render_template('preload.html')


# ---- Main Page --- #
@app.route('/portfolio/data-science/box-office', methods=["GET", "POST"])
def boxoffice_report():
    logout_user()
    movie_lookup_form = MovieLookupForm()
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URI", "sqlite:///movies.db")

    # -- Interactive Section -- #
    if request.method == "POST":
        movie = request.form['movie']
        year = request.form['release_year']
        alt = request.form['streaming']
        try:
            requested_html_table, requested_dataframe = get_boxoffice_and_trends_table(movie=movie, year=year, alt=alt)
            requested_chart = get_boxoffice_and_trends_figure(dataframe=requested_dataframe)
            return render_template('datascience_boxoffice.html',
                                   form=movie_lookup_form,
                                   get_chart_for=get_chart_from_database,
                                   action='show_table',
                                   requested_table=requested_html_table,
                                   requested_chart=requested_chart,
                                   movie=movie,
                                   get_movie_poster=get_movie_poster,
                                   get_movie_date=get_movie_date,
                                   get_movie_blurb=get_movie_blurb,
                                   )
        except (IndexError, TypeError):
            flash(f'Please double check the spelling of the movie and the release year entered, and try again.')
            return redirect(url_for('boxoffice_report'))

    return render_template('datascience_boxoffice.html',
                           form=movie_lookup_form,
                           get_chart_for=get_chart_from_database,
                           get_movie_poster=get_movie_poster,
                           get_movie_date=get_movie_date,
                           get_movie_blurb=get_movie_blurb,
                           )
# -------- END DATA SCIENCE BOX OFFICE -------- #


@app.errorhandler(404)
def not_found(error):
    return redirect(url_for("home_page"))

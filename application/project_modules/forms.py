from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, TextAreaField, PasswordField, URLField, DateTimeField, \
    SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo


# ---- For Main Web Pages ---- #
class ContactForm(FlaskForm):
    name = StringField(label='Name:', validators=[DataRequired()])
    email = StringField(label='Email:', validators=[DataRequired(),
                                                    Email(message="Please enter a valid email.")])
    subject = StringField(label='Subject:', validators=[DataRequired(), Length(max=70)])
    message = TextAreaField(label='Message:', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


# ---- For Tarot Reader ---- #
class LoginForm(FlaskForm):
    username = StringField(label='Username:')
    email = EmailField(label='Email:', validators=[DataRequired(),
                                                   Email(message="Please enter a valid email.")])
    password = PasswordField(label='Password:', id='password')


class ResetPasswordForm(FlaskForm):
    username = StringField(label='Username:')
    password = PasswordField(label='Password:', id='password',
                             validators=[DataRequired(),
                                         EqualTo('confirm_password')
                                         ])
    confirm_password = PasswordField(label='Confirm Password:', id='confirm_password')


class AddMessageForm(FlaskForm):
    message = TextAreaField(label='Message:', validators=[DataRequired(), Length(max=140)])


# ---- For Robots.Txt Checker ---- #
class EnterWebsiteForm(FlaskForm):
    url = URLField(label='Enter A URL:', validators=[DataRequired()],
                   render_kw={'placeholder': "Be sure to include 'https://'... It may be easier to paste in the url"})


# ---- For Data Science Box-Office ---- #
class MovieLookupForm(FlaskForm):
    movie = StringField(label='Movie:', validators=[DataRequired()])
    release_year = DateTimeField(label="Release Year:", format='%Y')
    streaming = SelectField(label='Streaming?',
                            choices=['Watch Online', 'HBO Max', 'Disney Plus', 'Netflix', 'Amazon Prime Video',
                                     'Peacock', 'Paramount Plus'],
                            render_kw={'placeholder': 'Watch Online'})

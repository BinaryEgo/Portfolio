import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ---- Keys, Passwords, Etc. ---- #

# dotenv.load_dotenv("C:/_CODING/Python/portfolio_passcodes.env")
# MY_EMAIL = os.getenv("gmail_1_email")
# PASSWORD = os.getenv("gmail_1_password")
#
# WEBSITE = 'http://127.0.0.1:5000'

MY_EMAIL = os.environ.get("gmail_1_email")
PASSWORD = os.environ.get("gmail_1_password")
WEBSITE = 'https://jermy-portfolio.herokuapp.com'


# ---- Contact Form ---- #
def send_email(contact_form):
    from_email = contact_form.email.data
    subject = contact_form.subject.data
    message = f"{contact_form.message.data}\n\nSent From:\n{contact_form.name.data}\n{contact_form.email.data}"

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=from_email,
            to_addrs=MY_EMAIL,
            msg=f"Subject: {subject}\n\n"
                f"{message}"
        )


# ---- Portfolio - Tarot Card Reset Password Email --- #
def send_reset_pw_email(requester_email, requester_name, link):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Reset Password Link - Jermy's Tarot Card Project"
    msg['From'] = MY_EMAIL
    msg['To'] = requester_email

    text = f"Hello!\n" \
           f"In case you forgot, your username is {requester_name}.\n" \
           f"You can reset your password in my Tarot Card project by clicking this link:{link}\n" \
           f"If you did not make this request, then ignore this e-mail and nothing will change."

    html = f"""
    <html>
        <head></head>
        <body>
            <p>
            Hello! In case you forgot, your <strong>username</strong> is [ <strong>{requester_name}</strong> ].
            <br><br>
            You can reset your password in my Tarot Card project by clicking this link:
            <br><br>
            <a href="{WEBSITE}{link}">Click Here to Reset Password</a>
            <br><br>
            If you did not make this request, then ignore this e-mail and nothing will change.    
            </p>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=requester_email,
            msg=msg.as_string()
        )


# ---- Portfolio - Submit Tarot Message --- #
def submit_tarot_message(message, user, link):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Tarot Card Project - Add A New Message"
    msg['From'] = MY_EMAIL
    msg['To'] = MY_EMAIL

    text = f"{message}\nSent by{user}.\n\n To accept click here: {link}"

    html = f"""
    <html>
        <head></head>
        <body>
            <p>
            "{message}"
            <br><br>
            Sent by: {user}.
            <br><br>
            <a href="{WEBSITE}{link}">Click Here to Accept</a>
    """

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP('smtp.gmail.com', 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(
            from_addr=MY_EMAIL,
            to_addrs=MY_EMAIL,
            msg=msg.as_string()
        )

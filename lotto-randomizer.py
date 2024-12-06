import os
import random
import smtplib
from email.mime.text import MIMEText

def pick_numbers(range_max, count):
    return tuple(sorted(random.sample(range(1, range_max+1), count)))

def pick_lotto_max():
    # Lotto Max: 7 numbers from 1 to 50
    return pick_numbers(50, 7)

def pick_daily_grand():
    # Daily Grand: 5 numbers from 1 to 49 plus 1 from 1 to 7
    main = pick_numbers(49, 5)
    grand = random.randint(1,7)
    return main + (grand,)

draw_type = os.environ.get("DRAW_TYPE")
target_draw = os.environ.get("TARGET_DRAW")

email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT")
recipient_2 = os.environ.get("RECIPIENT_2")

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_user, email_pass)
        server.send_message(msg)

if draw_type == "DAILY_GRAND":
    # Only one set, one recipient
    picks = pick_daily_grand()
    subject = f"Daily Grand Picks for {target_draw}"
    body = f"Daily Grand picks for {target_draw}: {picks}"
    send_email(subject, body, recipient)

elif draw_type == "LOTTO_MAX":
    # Two sets: one for RECIPIENT, one for RECIPIENT_2
    picks_main = pick_lotto_max()
    picks_second = pick_lotto_max()

    subject_main = f"Lotto Max Picks for {target_draw}"
    body_main = f"Lotto Max picks for {target_draw}: {picks_main}"
    send_email(subject_main, body_main, recipient)

    subject_second = f"Lotto Max Picks for {target_draw} (Second Set)"
    body_second = f"Lotto Max picks (second set) for {target_draw}: {picks_second}"
    send_email(subject_second, body_second, recipient_2)
else:
    # No draw
    pass


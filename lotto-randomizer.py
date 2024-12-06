import os
import sys
import smtplib
from email.mime.text import MIMEText

email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")
recipient = os.environ.get("RECIPIENT")
recipient_2 = os.environ.get("RECIPIENT_2")
draw_type = os.environ.get("DRAW_TYPE")
target_draw = os.environ.get("TARGET_DRAW")

def pick_numbers(range_max, count):
    import random
    return tuple(sorted(random.sample(range(1, range_max+1), count)))

def pick_lotto_max():
    # Lotto Max: 7 distinct numbers from 1 to 50
    return pick_numbers(50, 7)

def pick_daily_grand():
    # Daily Grand: 5 distinct numbers from 1 to 49 plus 1 from 1 to 7
    main = pick_numbers(49, 5)
    import random
    grand = random.randint(1,7)
    return main + (grand,)

def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = email_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            # Attempt to log in
            server.login(email_user, email_pass)
            # Attempt to send message
            refused = server.send_message(msg)
            # Check if any recipients were refused
            if refused:
                print("Email sent, but some recipients were refused:", refused)
                sys.exit(1)
    except smtplib.SMTPAuthenticationError as e:
        print("SMTP Authentication failed. Check EMAIL_USER and EMAIL_PASS.")
        print("Error details:", e)
        sys.exit(1)
    except smtplib.SMTPException as e:
        print("SMTP-related error occurred:", e)
        sys.exit(1)
    except Exception as e:
        print("An unexpected error occurred while sending email:", e)
        sys.exit(1)

if draw_type == "DAILY_GRAND":
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
    # If there's no draw type set, exit gracefully (or consider failing since no email was sent)
    print("No draw type set for today. No email sent.")
    # Exit 0 because this may be an expected scenario on certain days
    sys.exit(0)

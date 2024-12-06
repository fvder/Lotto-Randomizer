import os
import random
import smtplib
from email.mime.text import MIMEText

def pick_numbers(range_max, count):
    return tuple(sorted(random.sample(range(1, range_max+1), count)))

def pick_lotto_max():
    # 7 numbers from 1 to 50
    return pick_numbers(50, 7)

def pick_daily_grand():
    # 5 numbers from 1 to 49 plus 1 number from 1 to 7
    main_numbers = pick_numbers(49, 5)
    grand_number = random.randint(1,7)
    return main_numbers + (grand_number,)

# Generate tickets
# Sunday: Monday Daily Grand
dg_sun = pick_daily_grand()
# Monday: Tuesday Lotto Max (two sets)
lm_mon = pick_lotto_max()
lm_mon_2 = pick_lotto_max()
# Wednesday: Thursday Daily Grand
dg_wed = pick_daily_grand()
# Thursday: Friday Lotto Max (two sets)
lm_thu = pick_lotto_max()
lm_thu_2 = pick_lotto_max()

lines_primary = []
lines_primary.append("Sunday for Monday Daily Grand: " + str(dg_sun))
lines_primary.append("Monday for Tuesday Lotto Max: " + str(lm_mon))
lines_primary.append("Wednesday for Thursday Daily Grand: " + str(dg_wed))
lines_primary.append("Thursday for Friday Lotto Max: " + str(lm_thu))

body_primary = "\n".join(lines_primary)

# Send first email (primary recipient)
msg_primary = MIMEText(body_primary)
msg_primary["Subject"] = "Lottery Sets"
msg_primary["From"] = os.environ.get("EMAIL_USER")
msg_primary["To"] = os.environ.get("RECIPIENT")

# For the second Lotto Max sets (Monday and Thursday only)
lines_secondary = []
lines_secondary.append("Monday for Tuesday Lotto Max (Second Set): " + str(lm_mon_2))
lines_secondary.append("Thursday for Friday Lotto Max (Second Set): " + str(lm_thu_2))

body_secondary = "\n".join(lines_secondary)

# Send second email (second recipient)
msg_secondary = MIMEText(body_secondary)
msg_secondary["Subject"] = "Lottery Sets (Second Lotto Max Sets)"
msg_secondary["From"] = os.environ.get("EMAIL_USER")
msg_secondary["To"] = os.environ.get("RECIPIENT_2")

email_user = os.environ.get("EMAIL_USER")
email_pass = os.environ.get("EMAIL_PASS")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(email_user, email_pass)
    server.send_message(msg_primary)
    server.send_message(msg_secondary)

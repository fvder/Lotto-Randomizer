import random
import smtplib
from email.mime.text import MIMEText
import os

main_numbers = [1,2,6,8,9,12,19,20,22]

all_daily_grand_sets = set()
all_lotto_max_sets = set()

def get_set(source, size, used_sets):
    attempts = 0
    while attempts < 10000:
        s = tuple(sorted(random.sample(source, size)))
        if s not in used_sets:
            used_sets.add(s)
            return s
        attempts += 1
    # If no new set can be found, reset
    used_sets.clear()
    s = tuple(sorted(random.sample(source, size)))
    used_sets.add(s)
    return s

# Sunday for Monday Daily Grand: 5 from main_numbers + 1 from 1 to 7
dg_sun = get_set(main_numbers, 5, all_daily_grand_sets) + (random.randint(1,7),)
# Monday for Tuesday Lotto Max: 7 from main_numbers
lm_mon = get_set(main_numbers, 7, all_lotto_max_sets)
# Wednesday for Thursday Daily Grand: 5 from main_numbers + 1 from 1 to 7
dg_wed = get_set(main_numbers, 5, all_daily_grand_sets) + (random.randint(1,7),)
# Thursday for Friday Lotto Max: 7 from main_numbers
lm_thu = get_set(main_numbers, 7, all_lotto_max_sets)

lines = []
lines.append("Sunday for Monday Daily Grand: " + str(dg_sun))
lines.append("Monday for Tuesday Lotto Max: " + str(lm_mon))
lines.append("Wednesday for Thursday Daily Grand: " + str(dg_wed))
lines.append("Thursday for Friday Lotto Max: " + str(lm_thu))

body = "\n".join(lines)

msg = MIMEText(body)
msg["Subject"] = "Lottery Sets"
msg["From"] = os.environ.get("EMAIL_USER")
msg["To"] = os.environ.get("RECIPIENT")

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(os.environ.get("EMAIL_USER"), os.environ.get("EMAIL_PASS"))
    server.send_message(msg)
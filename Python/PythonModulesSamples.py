#JSON_Manipulation.py

import json


with open('example.json','r') as f:
    data = json.load(f)

print(data)



data = {'name':'John','age':30,'city':'New York'}
with open('test.json','w') as f:
    json.dump(data, f, indent=4)


now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"))

#Threading_Sample.py
import threading
import time

def print_number():
    for i in range(5):
        print(i)
        #time.sleep(1)

thread = threading.Thread(target=print_number)
thread.start()
thread.join()

import schedule
import time

def job():
    print("I'm working...")

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)

"""
Mini Project
Regular backups prevent data loss. Create a script that automates file backups at set intervals.
"""

#Email_Send_Retrieve.py


"""import smtplib
from email.mime.text import MIMEText"""

"""
def send_email(subject, body, to_email):
    from_email = "avirup@dataengineeracademy.com" 
    password = "gvvg iaua imtn mfqc"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    with smtplib.SMTP_SSL('smtp.gmail.com',465) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

send_email("Test Subject","This is a test email", "avirup@dataengineeracademy.com")
"""

import imaplib
import email

def retrieve_emails():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login("avirup@dataengineeracademy.com","kjfg yvay wjbn citc")
    mail.select('inbox')


    typ,data = mail.search(None, 'ALL')
    email_ids = data[0].split()


    for email_id in email_ids:
        typ,data = mail.fetch(email_id,'(RFC822)')
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)

        print(f"From:{msg['From']}")
        print(f"Subject:{msg['Subject']}")

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if part.get_content_type == 'text/plain' and "attachment" not in content_disposition:
                    payload = part.get_payload(decode=True)
                    if payload:
                        try:
                            print(payload.decode())
                        except UnicodeDecodeError:
                            print("Could not decode this part.")
                    else:
                        msg.get_payload(decode=True)
                        if payload:
                            print(payload.decode())
                        else:
                            print("No decodable payload found")
    mail.close()
    mail.logout()

retrieve_emails()
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailNotifier:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER')
        self.smtp_port = int(os.getenv('SMTP_PORT'))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL')
        self.to_email_list_file = 'to_email_list.txt'
        self.load_email_list()

    def load_email_list(self):
        if not os.path.exists(self.to_email_list_file):
            with open(self.to_email_list_file, 'w') as f:
                pass
        with open(self.to_email_list_file, 'r') as f:
            self.to_email_list = [line.strip() for line in f if line.strip()]

    def save_to_email_list(self):
        with open(self.to_email_list_file, 'w') as f:
            for email in self.to_email_list:
                f.write(f"{email}\n")

    def add_recipient(self, email):
        if email not in self.to_email_list:
            self.to_email_list.append(email)
            self.save_to_email_list()

    def send_email(self, subject, body):
        if not self.to_email_list:
            print("No recipients to send email to.")
            return

        msg = MIMEMultipart()
        msg['From'] = self.from_email
        msg['To'] = ', '.join(self.to_email_list)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        server.starttls()
        server.login(self.smtp_username, self.smtp_password)
        text = msg.as_string()
        server.sendmail(self.from_email, self.to_email_list, text)
        server.quit()
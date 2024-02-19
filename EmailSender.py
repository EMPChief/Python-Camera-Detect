import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import dotenv
import os
dotenv.load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv("email_host")
        self.smtp_port = int(os.getenv("email_port"))
        self.smtp_username = os.getenv("email_mail")
        self.smtp_password = os.getenv("email_pass")

    def send_email(self, subject, body, recipient_email):
        print(f"Sending email to {recipient_email}...")
        email_message = MIMEMultipart()
        email_message['From'] = self.smtp_username
        email_message['To'] = recipient_email
        email_message['Subject'] = subject

        if isinstance(body, str):
            body = body.encode('utf-8')

        email_message.attach(MIMEText(body.decode('utf-8'), 'plain'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(self.smtp_username, self.smtp_password)
                smtp_server.sendmail(
                    self.smtp_username, recipient_email, email_message.as_string())
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

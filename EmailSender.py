import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os
from dotenv import load_dotenv

load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = os.getenv("email_host")
        self.smtp_port = int(os.getenv("email_port"))
        self.smtp_username = os.getenv("email_mail")
        self.smtp_password = os.getenv("email_pass")

        if not all([self.smtp_server, self.smtp_port, self.smtp_username, self.smtp_password]):
            raise ValueError("Email configuration is incomplete. Please check your environment variables.")

    def send_email(self, subject, body, recipient_email, image_path=None):
        print(f"Sending email to {recipient_email}...")
        email_message = MIMEMultipart()
        email_message['From'] = self.smtp_username
        email_message['To'] = recipient_email
        email_message['Subject'] = subject

        if isinstance(body, str):
            body = body.encode('utf-8')

        email_message.attach(MIMEText(body.decode('utf-8'), 'plain'))

        if image_path:
            try:
                with open(image_path, 'rb') as img_file:
                    img_data = img_file.read()
                image = MIMEImage(img_data, name=os.path.basename(image_path))
                email_message.attach(image)
            except Exception as e:
                print(f"Error attaching image: {e}")

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as smtp_server:
                smtp_server.starttls()
                smtp_server.login(self.smtp_username, self.smtp_password)
                smtp_server.sendmail(
                    self.smtp_username, recipient_email, email_message.as_string())
            print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False


if __name__ == "__main__":
    EmailSender().send_email(
        subject="Testing",
        body="This is a test email.",
        recipient_email="support@empchief.com",
        image_path="image.jpg"
    )

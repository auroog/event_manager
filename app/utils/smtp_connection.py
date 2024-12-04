# smtp_client.py
from builtins import Exception, int, str
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from settings.config import settings
import logging

class SMTPClient:
    def __init__(self, server: str, port: int, username: str, password: str):
        self.server = server
        self.port = port
        self.username = username
        self.password = password

    def send_email(
        self,
        subject: str,
        html_content: str,
        recipient: str,
        cc: list[str] = None,
        bcc: list[str] = None
    ):
        """
        Send an email with the given subject and HTML content to the recipient.

        Args:
            subject (str): Subject of the email.
            html_content (str): HTML content of the email.
            recipient (str): Primary recipient email address.
            cc (list[str], optional): List of CC recipients. Defaults to None.
            bcc (list[str], optional): List of BCC recipients. Defaults to None.
        """
        try:
            # Prepare email message
            message = MIMEMultipart('alternative')
            message['Subject'] = subject
            message['From'] = self.username
            message['To'] = recipient

            if cc:
                message['Cc'] = ", ".join(cc)
            recipients = [recipient] + (cc or []) + (bcc or [])

            # Attach the HTML content
            message.attach(MIMEText(html_content, 'html'))

            # Send the email
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()  # Use TLS
                server.login(self.username, self.password)
                server.sendmail(self.username, recipients, message.as_string())

            logging.info(f"Email successfully sent to {recipient} with subject '{subject}'.")
        except smtplib.SMTPException as smtp_err:
            logging.error(f"SMTP error while sending email: {str(smtp_err)}")
            raise
        except Exception as e:
            logging.error(f"Failed to send email due to an unexpected error: {str(e)}")
            raise

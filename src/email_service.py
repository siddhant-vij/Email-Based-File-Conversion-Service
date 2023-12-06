import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from dotenv import load_dotenv
import re
from converter_service import convert_docx_to_pdf


class EmailService:
    def __init__(self):
        load_dotenv()
        self.user = os.getenv('EMAIL_USER')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.imap_url = os.getenv('IMAP_SERVER')
        self.smtp_url = os.getenv('SMTP_SERVER')

    def connect_to_email(self):
        self.mail = imaplib.IMAP4_SSL(self.imap_url)
        self.mail.login(self.user, self.password)
        self.mail.select('inbox')

    def process_emails(self):
        status, email_ids = self.mail.search(None, 'UNSEEN')
        if status != 'OK':
            print("No new emails to process.")
            return

        for e_id in email_ids[0].split():
            _, data = self.mail.fetch(e_id, '(RFC822)')
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            subject = msg['Subject']
            format_from, format_to = self.parse_subject(subject)

            if format_from and format_to:
                if not self.is_supported_format(format_from, format_to):
                    self.send_failure_email(
                        msg['From'], format_from, format_to, "Unsupported file format conversion requested.")
                    continue

                attachment_found = False
                for part in msg.walk():
                    if part.get_content_maintype() == 'multipart' or part.get('Content-Disposition') is None:
                        continue
                    file_name = part.get_filename()
                    if file_name and self.is_correct_attachment(file_name, format_from):
                        file_data = part.get_payload(decode=True)
                        self.handle_conversion(
                            file_name, file_data, format_from, format_to, msg['From'])
                        attachment_found = True
                        break

                if not attachment_found:
                    self.send_failure_email(
                        msg['From'], format_from, format_to, "No suitable attachment found.")

    def is_supported_format(self, format_from, format_to):
        supported_conversions = [("DOCX", "PDF")]
        return (format_from.upper(), format_to.upper()) in supported_conversions

    def is_correct_attachment(self, file_name, format_from):
        file_extension = os.path.splitext(file_name)[1][1:].upper()
        return file_extension == format_from.upper()

    def send_failure_email(self, recipient, format_from, format_to, reason):
        subject = "Conversion Failed"
        body = f"Failed to convert from {format_from} to {format_to}. Reason: {reason}"
        self.send_email(recipient, subject, body)

    def handle_conversion(self, file_name, file_data, format_from, format_to, recipient_email):
        source_path = 'temp/' + file_name
        output_path = self.get_output_path(file_name, format_to)

        # Save the attachment to a temporary file
        with open(source_path, 'wb') as file:
            file.write(file_data)

        # Handle different conversion types
        if format_from == 'DOCX' and format_to == 'PDF':
            convert_docx_to_pdf(source_path, output_path)
            self.send_email(recipient_email, "Converted file",
                            "Here's your PDF", output_path)
        else:
            self.send_email(recipient_email, "Conversion Failed",
                            f"Conversion from {format_from} to {format_to} is not supported yet.")

        # Clean up temporary files
        os.remove(source_path)
        if os.path.exists(output_path):
            os.remove(output_path)

    def get_output_path(self, file_name, format_to):
        base_name = os.path.splitext(file_name)[0]
        return 'temp/' + base_name + '.' + format_to.lower()

    def parse_subject(self, subject):
        match = re.match(r"\[(.*)\] to \[(.*)\]", subject)
        if match:
            return match.groups()
        return None, None

    def send_email(self, to, subject, body, attachment=None):
        msg = MIMEMultipart()
        msg['From'] = self.user
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        if attachment:
            with open(attachment, 'rb') as f:
                part = MIMEApplication(
                    f.read(), Name=os.path.basename(attachment))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
            msg.attach(part)

        server = smtplib.SMTP(self.smtp_url, 587)
        server.starttls()
        server.login(self.user, self.password)
        server.send_message(msg)
        server.quit()

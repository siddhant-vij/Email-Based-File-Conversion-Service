from flask import Flask
from email_service import EmailService
import threading
import time

app = Flask(__name__)
email_service = EmailService()

# Visit http://127.0.0.1:5000/ in your browser.


def check_emails_periodically():
    while True:
        email_service.connect_to_email()
        email_service.process_emails()
        time.sleep(10)  # Check emails every 10 seconds


@app.route('/')
def index():
    return "Email Conversion Service is running."


if __name__ == "__main__":
    email_thread = threading.Thread(target=check_emails_periodically)
    email_thread.start()
    app.run(debug=True, use_reloader=False)

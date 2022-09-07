# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

message = Mail(
    from_email='benchmarklabbot1@gmail.com',
    to_emails='raymondzoubenchmark@gmail.com',
    subject='Test',
    html_content='EMAIL WARNING SETUP')
try:
    sg = SendGridAPIClient(os.environ.get('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'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(e.message)
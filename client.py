import smtplib
import email.utils
from email.mime.text import MIMEText

# Create the message
msg = MIMEText('Body of the message.')
msg['To'] = email.utils.formataddr(('Recipient', 'to@bitnation.co'))
msg['From'] = email.utils.formataddr(('Author', 'from@bitnation.co'))
msg['Subject'] = 'Simple test message'

server = smtplib.SMTP('127.0.0.1', 1025)
server.set_debuglevel(True) # show communication with the server
try:
    server.sendmail('from@bitnation.co', ['to@bitnation.com'], msg.as_string())
finally:
    server.quit()

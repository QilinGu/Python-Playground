import smtplib
import os
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate


def send_mail(send_from, send_to, subject, text, files=None):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    email = os.environ['GMAIL_USERNAME']
    password = os.environ['GMAIL_PASSWORD']

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            msg.attach(part)

    
    smtp = smtplib.SMTP('smtp.gmail.com',587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(email, password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

if __name__ == "__main__":
    send_from = 'gump423@gmail.com'
    send_to = ['gump423@gmail.com']
    subject = 'SSH keys for boedev3'
    text = 'Sending SSH keys settings for boedev3'
    files = ['sshkeys.zip']
    send_mail(send_from, send_to, subject, text, files)

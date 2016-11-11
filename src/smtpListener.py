import smtpd, subprocess, os, tempfile, io
import sendgrid
from sendgrid.helpers.mail import *

def sendMail(sender, receiver, subject, message):
    print("Email to <" + receiver + "> from <" + sender + "> intercepted")
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender)
    to_email = Email(receiver)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code

def editMail(message, mailfrom, rcpttos):
    subject = "foo"
    buf = io.StringIO(message)
    line = buf.readline()
    while not line.startswith("Subject: ") and len(line) > 0:
        line = buf.readline()
    subject = line[9:]

    with tempfile.NamedTemporaryFile(delete = False) as f:
        f.write(str.encode(message))
        f.close()
        cmd = os.environ.get('EDITOR', 'vi') + ' ' + f.name
        subprocess.call(cmd, shell=True)
        with open(f.name) as dataFile:
            sendMail(mailfrom, rcpttos[0], subject, dataFile.read())
            dataFile.close()

class SmtpListener(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        editMail(data, mailfrom, rcpttos)
        return

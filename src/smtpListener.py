import smtpd, subprocess, os, tempfile
import sendgrid
from sendgrid.helpers.mail import *

def sendMail(sender, receiver, subject, message):
    print(sender)
    print(receiver)
    print(subject)
    print(message)
    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender)
    to_email = Email(receiver)
    content = Content("text/plain", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    return response.status_code

def editMail(message, mailfrom, rcpttos):
    with tempfile.NamedTemporaryFile(delete = False) as f:
        f.write(str.encode(message))
        f.close()
        cmd = os.environ.get('EDITOR', 'vi') + ' ' + f.name
        subprocess.call(cmd, shell=True)
        with open(f.name) as dataFile:
            sendMail(mailfrom, rcpttos[0], "test", dataFile.read())
            dataFile.close()

class SmtpListener(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        editMail(data, mailfrom, rcpttos)
        return

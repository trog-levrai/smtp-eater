import smtpd, subprocess, os, tempfile

def editMail(message):
    with tempfile.NamedTemporaryFile(delete = False) as f:
        f.write(str.encode(message))
        f.close()
        cmd = os.environ.get('EDITOR', 'vi') + ' ' + f.name
        subprocess.call(cmd, shell=True)
        with open(f.name) as dataFile:
            print(dataFile.read())
            dataFile.close()


class SmtpListener(smtpd.SMTPServer):

    def process_message(self, peer, mailfrom, rcpttos, data):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to  :', rcpttos)
        print('Message length        :', len(data))
        editMail(data)
        return

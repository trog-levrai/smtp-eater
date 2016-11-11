import os, subprocess, tempfile, asyncore
from smtpListener import *

server = SmtpListener(('127.0.0.1', 1025), None)

asyncore.loop()

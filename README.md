# smtp-eater

Performs a basic man in the middle attack on sent emails

Simply set smtp server of your email client on port 1095 and your default editor will be opened when an email is sent through your smtp server.

When saving and quitting, the email will be sent using Sendgrid SMTP servers.

To send emails you need to have a Sendgrid API key and export it under *SENDGRID_API_KEY* environment variable.

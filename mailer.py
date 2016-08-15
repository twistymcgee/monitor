import smtplib

class Mailer:
    def __init__(self, smtpserver):

        self.smtpserver = smtpserver

    def sendmail(self, to_address, from_address, subject, message):
        print("Sending message")
        server = smtplib.SMTP(self.smtpserver)
        #server.ehlo()
        #server.starttls()
        msg = "\r\n".join([
            "From: " + from_address,
            "To: " + to_address,
            "Subject: " + subject,
            "",
            message
        ])
        server.sendmail(from_address, to_address, msg)
        server.quit()

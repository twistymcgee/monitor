import smtplib, logging

class Mailer:
    def __init__(self, smtpserver, to_address, from_address):
        self.logger = logging.getLogger('MonitorApp.Mailer')
        self.smtpserver = smtpserver
        self.to_address = to_address
        self.from_address = from_address

    def sendmail(self, subject, message):
        self.logger.info("Sending message")
        server = smtplib.SMTP(self.smtpserver)
        msg = "\r\n".join([
            "From: " + self.from_address,
            "To: " + self.to_address,
            "Subject: " + subject,
            "",
            message
        ])
        server.sendmail(self.from_address, self.to_address, msg)
        server.quit()

import smtplib, logging
from config_exception import ConfigException

class Mailer:
    def __init__(self, config):
        self.logger = logging.getLogger('MonitorApp.Mailer')
        self.parse_config(config)

    def parse_config(self, config):
        self.validate_config(config)
        self.smtpserver = config['smtphost']
        self.to_address = config['to_address']
        self.from_address = config['from_address']

    def validate_config(self, config):
        if ('smtphost' not in config):
            raise ConfigException("Mailer config missing 'smtphost'")
        if ('to_address' not in config):
            raise ConfigException("Mailer config missing 'to_address'")
        if ('from_address' not in config):
            raise ConfigException("Mailer config missing 'from_address'")

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

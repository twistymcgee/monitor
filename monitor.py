import http.client, os, logging, socket
from config_exception import ConfigException

class Monitor:
    def __init__(self, notifier, config):
        self.logger = logging.getLogger('MonitorApp.Monitor')
        self.parse_config(config)
        self.reason = None
        self.notifier = notifier

    def parse_config(self, config):
        self.validate_config(config)
        self.service_name = config['name']
        self.url = config['host']
        if 'port' not in config:
            # default to 80
            self.logger.info("'port' not specified in config for '%s', defaulting to 80", self.service_name)
            self.port = 80
        else:
            self.port = config['port']
        self.string_to_find = config['find_string']
        if 'timeout' not in config:
            # default to 20 seconds
            self.logger.info("'timeout' not specified in config for '%s', defaulting to 20 seconds", self.service_name)
            self.timeout = 20
        else:
            self.timeout = config['timeout']

    def validate_config(self, config):
        if ('name' not in config):
            raise ConfigException("Monitor config missing 'name'")
        if ('host' not in config):
            raise ConfigException("Monitor config missing 'host'")
        if ('find_string' not in config):
            raise ConfigException("Monitor config missing 'find_string'")

    def check(self):
        self.logger.info('Checking service %s url %s port %d', self.service_name, self.url, self.port)
        try:
            connection = http.client.HTTPConnection(self.url, self.port, timeout=self.timeout)
            connection.connect()
            connection.request('GET', '/')
            response = connection.getresponse()
            html = response.read().decode()
            result = html.find(self.string_to_find)
            if (result > -1):
                self.set_up_state()
            else:
                self.reason = 'Response did not contain string ' + self.string_to_find
                self.set_down_state()
        except ConnectionRefusedError:
            self.reason = 'Connection refused'
            self.set_down_state()
        except socket.timeout:
            self.reason = 'Timed out'
            self.set_down_state()
        except OSError as err:
            self.reason = err.args[1]
            self.set_down_state()

    def set_up_state(self):
        self.logger.info("%s Up", self.service_name)
        # if previously in a failed state, change it
        if self.in_failed_state():
            self.remove_token_file()
            self.notifier.sendmail(self.service_name + ' Up', self.service_name + " Up!")

    def set_down_state(self):
        self.logger.info("%s Down! %s", self.service_name, self.get_reason())
        if not self.in_failed_state():
            self.create_token_file()
            self.notifier.sendmail(self.service_name + ' Down', self.service_name + " Down! " + self.get_reason())

    def get_reason(self):
        return self.reason

    def create_token_file(self):
        if not os.path.exists(self.service_name):
            open(self.service_name, 'w+').close()

    def remove_token_file(self):
        if os.path.exists(self.service_name):
            os.remove(self.service_name)

    def in_failed_state(self):
        if os.path.exists(self.service_name):
            return True
        return False

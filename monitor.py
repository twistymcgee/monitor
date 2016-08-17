import http.client, os, logging, socket

class Monitor:
    def __init__(self, notifier, config):
        self.logger = logging.getLogger('MonitorApp.Monitor')
        self.service_name = config['name']
        self.url = config['host']
        self.port = config['port']
        self.string_to_find = config['find_string']
        self.timeout = config['timeout']
        self.reason = None
        self.notifier = notifier

    def check(self):
        self.logger.info('Checking service ' + self.service_name + ' url ' + self.url)
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
        self.logger.info(self.get_service_name() + " Up")
        # if previously in a failed state, change it
        if self.in_failed_state():
            self.remove_token_file()
            self.notifier.sendmail(self.get_service_name() + ' Up', self.get_service_name() + " Up!")

    def set_down_state(self):
        self.logger.info(self.get_service_name() + " Down! " + self.get_reason())
        if not self.in_failed_state():
            self.create_token_file()
            self.notifier.sendmail(self.get_service_name() + ' Down', self.get_service_name() + " Down! " + self.get_reason())


    def get_reason(self):
        return self.reason

    def get_service_name(self):
        return self.service_name

    def create_token_file(self):
        if not os.path.exists(self.get_service_name()):
            open(self.get_service_name(), 'w+').close()

    def remove_token_file(self):
        if os.path.exists(self.get_service_name()):
            os.remove(self.get_service_name())

    def in_failed_state(self):
        if os.path.exists(self.get_service_name()):
            return True
        return False

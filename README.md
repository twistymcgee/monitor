# monitor

A simple app that monitors whether a webservice is up.

### Usage
Setup the following command to run in a crontab

```bash
run_monitor -c <path to>/monitor.yml
```

### Config file
The config file is a yaml file with the following entries:

```yaml
log:
  file: /<path to log file>/monitor.log
mailer:
  smtphost: <your smtp server>
  to_address: <email to notify>
  from_address: <email to send from>
monitors:
  - name: Service1
    host: <service host name>
    port: <service port>
    find_string: <string to look for indicating up>
  - name: Service1
    host: <service host name>
    port: <service port>
    find_string: <string to look for indicating up>
```

You can have as many monitors as you want.

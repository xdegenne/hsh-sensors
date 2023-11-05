
#!/usr/bin/python3

# stdlib
from influxdb import InfluxDBClient
import datetime, time, logging

# Self libraries
import utils

log = logging.getLogger('hsh-sensors')

log.debug('Loading config...')
config = utils.load_config()

log.debug(f'Config loaded! Values: {config}')
period = int(config.get('period', 60))

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('hsh_sensors')

while True:
    log.debug("Cycle begins")

    log.debug(f"Cycle ends, sleeping for {period} seconds")
    time.sleep(period)    


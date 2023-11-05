
#!/usr/bin/python3

# stdlib
from influxdb import InfluxDBClient
import datetime, time, logging
import time
import board
import adafruit_dht
import psutil

# Self libraries
import utils

log = utils.init_log_system()

log.debug('Loading config...')
config = utils.load_config()

log.debug(f'Config loaded! Values: {config}')
period = int(config.get('period', 60))

client = InfluxDBClient(host='localhost', port=8086)
client.switch_database('hsh_sensors')

# We first check if a libgpiod process is running. If yes, we kill it!
for proc in psutil.process_iter():
    if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
        proc.kill()
sensor = adafruit_dht.DHT11(board.D17)

def read_sensor():
    value = None
    while value == None:
        temp = None
        humidity = None
        try:
            temp = sensor.temperature
            humidity = sensor.humidity
            log.debug(f"Temperature: {temp}*C   Humidity: {humidity}%")
            if temp != None and humidity != None:
                value = [
                    {
                        "measurement": "dhtEvents",
                        "tags": {
                            "sondeId": "D17"
                        },
                        "time": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S'),
                        "fields": {
                            "temperature": temp,
                            "humidity": humidity
                        }
                    }
                ]
        except RuntimeError as error:
            log.error(error.args[0])
        except Exception as error:
            sensor.exit()
            raise error
        if value == None:
            time.sleep(2.0)
        else:
            return value

while True:
    log.debug("Cycle begins")

    value = read_sensor()
    client.write_points(value)

    log.debug(f"Cycle ends, sleeping for {period} seconds")
    time.sleep(period)    


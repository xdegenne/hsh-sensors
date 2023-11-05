#!/usr/bin/python3

# stdlib
import serial, MySQLdb, datetime, sys, logging, logging.handlers

# 3rd party
import yaml


def init_log_system():
    """
    Initializes log system
    """
    log = logging.getLogger('hsh-sensors')
    log.setLevel(logging.DEBUG) # Define minimum severity here
    handler = logging.handlers.RotatingFileHandler('./logs/hsh-sensors.log', maxBytes=1000000, backupCount=5) # Log file of 1 MB, 5 previous files kept
    formatter = logging.Formatter('[%(asctime)s][%(module)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S %z') # Custom line format and time format to include the module and delimit all of this well
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def load_config():
    """
    Loads config file
    """
    try:
        with open('config.yml', 'r') as f:
            config = yaml.safe_load(f)
    except Exception as e:
        log.critical('Something went wrong while opening config file:', exc_info=True)
        print('Something went wrong while opening config file. See logs for more info.', file=sys.stderr)
        raise SystemExit(3)
    else:
        return config
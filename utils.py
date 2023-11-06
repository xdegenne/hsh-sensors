#!/usr/bin/python3

# stdlib
import sys, logging, logging.handlers
from systemd.journal import JournaldLogHandler

# 3rd party
import yaml

logLevels = {   'DEBUG': logging.DEBUG, 
                'INFO': logging.INFO,
                'WARNING': logging.WARNING,
                'ERROR': logging.ERROR,
                'CRITICAL': logging.CRITICAL,
            }

def init_log_system(config):
    """
    Initializes log system
    """
    logLevelStr = config.get('logLevel', 'WARNING')
    logLevel = logLevels.get(logLevelStr, logging.WARNING)
    log = logging.getLogger('hsh-sensors')
    log.setLevel(logLevel) # Define minimum severity here
    
    # instantiate the JournaldLogHandler to hook into systemd
    handler = JournaldLogHandler()

    # set a formatter to include the level name
    handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(message)s'
    ))

    # handler = logging.StreamHandler()
    # handler.setLevel(logLevel)

    #handler = logging.handlers.RotatingFileHandler('./logs/hsh-sensors.log', maxBytes=1000000, backupCount=5) # Log file of 1 MB, 5 previous files kept
    #formatter = logging.Formatter('[%(asctime)s][%(module)s][%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S %z') # Custom line format and time format to include the module and delimit all of this well
    #handler.setFormatter(formatter)
    log.addHandler(handler)
    #log.addHandler()
    log.info("Log initialized")
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
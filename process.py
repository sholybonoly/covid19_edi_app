# This is the main runner 
# Run this script to process the next batch of emails
# This could be run in a cron job to periodically check email box

import EmailRelayProcessor
import time
import configparser
import logging

if __name__ == "__main__":

    # get logging configuration from our config file
    config = configparser.ConfigParser()
    config.read('config.ini')

    logLevelString = config.get('LOGGING','LogLevel')

    # default log level value should be ERROR
    logLevel = logging.ERROR
    if (logLevelString == 'DEBUG'):
        logLevel = logging.DEBUG
    elif (logLevelString == 'INFO'):
        logLevel = logging.INFO
    elif (logLevelString == 'WARNING'):
        logLevel = logging.WARNING
    elif (logLevelString == 'ERROR'):
        logLevel = logging.ERROR
    elif (logLevelString == 'CRITICAL'):
        logLevel = logging.CRITICAL
    
    logFile = config.get('LOGGING','LogFile')
    if (logFile == None):
        logFile = "relay.log"
    
    # setup logging based on our config
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        filename=logFile,
        level=logLevel,
    )

    processor = EmailRelayProcessor.EmailRelayProcessor()
    processor.run()
    

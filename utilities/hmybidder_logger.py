import logging
import os

blsdir = '/home/satish/blsdir'
logDir = 'log'
logger = None
logfile = 'hmybidder.log'

class HmyBidderLog:

    def __init__(self):
        self.initializeLogger()

    @classmethod
    def initializeLogger(self):
        if not os.path.exists(logDir):
            os.makedirs(logDir)
        logging.basicConfig(filename=f'{logDir}/{logfile}', level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    @classmethod
    def setLogFileLocation(self, logfileLocation):
        #print(f"Logfile {logfileLocation}")
        if logfileLocation != '' and logfileLocation.endswith('.log'):
            logging.basicConfig(filename=logfileLocation, level=logging.INFO, format='%(asctime)s.%(msecs)03d : %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        else:
            raise Exception('Log File Exception', 'Invalid Logfile location')

    @classmethod
    def debug(self, msg):
        logging.debug(msg)

    @classmethod
    def info(self, msg):
        logging.info(msg)

    @classmethod
    def warning(self, msg):
        logging.warning(msg)

    @classmethod
    def error(self, msg):
        logging.error(msg)
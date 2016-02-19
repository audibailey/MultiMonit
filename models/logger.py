import xml.etree.cElementTree as ET
from models import Config
from site_config import SiteConfig
import urllib, os, time, logging, threading


class logs():

    @staticmethod
    def setup_logger(logger_name, log_file, level=logging.INFO):
        l = logging.getLogger(logger_name)
        formatter = logging.Formatter('%(asctime)s \n %(message)s')
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(formatter)

        l.setLevel(level)
        l.addHandler(fileHandler)
        l.addHandler(streamHandler)

    @staticmethod
    def log(m):
        refresh = 20

        config = Config.readconfig()
        refresh = config["refresh"]

        name = ""
        monit = ET.parse(urllib.urlopen(m)) or ET.parse(m)
        root = monit.getroot()

        for i in root.findall("server/localhostname"):
            name = i.text

        logs.setup_logger(name, SiteConfig.home + "/logs/" + name + '.txt')
        logger = logging.getLogger(name)

        while True:
            data = ET.tostring(root)
            logger.info(data)
            time.sleep(refresh)

    @staticmethod
    def logall():
        config = Config.readconfig()
        url = config["URLS"]

        if os.path.exists("logs"):
            pass
        else:
            os.mkdir("logs")

        thread_list = []

        for m in url:
            # Instantiates the thread
            # (i) does not make a sequence, so (i,)
            t = threading.Thread(target=logs.log, args=(m,))
            # Sticks the thread in a list so that it remains accessible
            thread_list.append(t)

        # Starts threads
        for thread in thread_list:
            thread.start()

        # This blocks the calling thread until the thread whose join() method is called is terminated.
        # From http://docs.python.org/2/library/threading.html#thread-objects
        for thread in thread_list:
            thread.join()


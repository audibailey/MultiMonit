import ConfigParser
import os

config = ConfigParser.RawConfigParser()
count = 0

def readConfig():
    URLS = []
    try:
        results = config.read("config.ini")
    except:
        print "Error Parsing File"
    else:
        if not results:
            pass
        else:
            for k, v in config.items("URLS"):
                URLS.append(v)
    return URLS


def readConfigRefresh():
    refresh = []
    try:
        results = config.read("config.ini")
    except:
        print "Error Parsing File"
    else:
        if not results:
            pass
        else:
            for k, v in config.items("Refresh"):
                refresh.append(v)
    return refresh


def makeConfig(Parameters):
    config.add_section('URLS')
    config.add_section('Refresh')
    config.set('Refresh', str(0), '20')
    for i in Parameters.values():
        global count
        config.set('URLS', str(count), i)
        count = count + 1

    with open('config.ini', 'wb') as configfile:
        config.write(configfile)


def mkfile(parameters):
    if os.path.exists("config.ini"):
        return None
    else:
        makeConfig(parameters)

def updateConfig(url, refresh):

    oldrefresh = readConfigRefresh()
    oldurl = readConfig()

    try:
        if refresh != oldrefresh:
            config.set('Refresh', str(0), refresh)

        if url != oldurl:
            for i in url.values():
                global count
                config.set('URLS', str(count), i)
                count = count + 1

        return 0
    except:
        return 1

import xml.etree.cElementTree as ET
from models import Config
import urllib


def system():

    url = Config.readConfig()
    print url

    parsed = []

    for m in url:
        data = {}
        de = []
        hostlst = []
        fs = []

        monit = ET.parse(urllib.urlopen(m)) or ET.parse(m)
        root = monit.getroot()


        for i in root.findall("*[@type='3']"):
            daemon = {h.tag: h.text for h in i if h.text != '\n            ' and h.text != '\n      ' and h.text != None and h.text != '\n          '}
            daemon.update({"mem": {h.tag: h.text for l in i.iter("memory") for h in l}})
            daemon.update({"cpu":{h.tag: h.text for l in i.iter("cpu") for h in l}})
            daemon.update({"port":{h.tag: h.text for l in i.iter("port") for h in l}})
            de.append(daemon)

        data.update({"process": de})

        for i in root.findall("*[@type='4']"):
            host = {h.tag: h.text for h in i if h.text != '\n            ' and h.text != '\n      ' and h.text != None and h.text != '\n          '}
            host.update({"port": {h.tag: h.text for l in i.iter("port") for h in l}})
            hostlst.append(host)

        data.update({"host": hostlst})

        for i in root.findall("*[@type='0']"):
            file = {h.tag: h.text for h in i if h.text != '\n            ' and h.text != '\n      ' and h.text != None and h.text != '\n          '}
            file.update({"block": {h.tag: h.text for l in i.iter("block") for h in l}})
            file.update({"inode": {h.tag: h.text for l in i.iter("inode") for h in l}})
            fs.append(file)

        data.update({"fs": fs})

        sys = {h.tag: h.text for i in root.findall("*[@type='5']") for h in i if h.text != '\n            ' and h.text != '\n      ' and h.text != None and h.text != '\n          '}
        sys.update({"load": {h.tag: h.text for i in root.findall("*[@type='5']/system/load") for h in i}, "cpu": {h.tag: h.text for i in root.findall("*[@type='5']/system/cpu") for h in i}, "memory":{h.tag: h.text for i in root.findall("*[@type='5']/system/memory") for h in i}, "swap":{h.tag: h.text for i in root.findall("*[@type='5']/system/swap") for h in i}, "server": {h.tag: h.text for i in root.findall("server") for h in i}, 'platform': {h.tag: h.text for i in root.findall('platform') for h in i}})
        data.update({"sys": sys})

        data.update({"url": '.'.join(str(m).replace('http://','').split('/')[0].split('.')[-2:])})
        parsed.append(data)

    return parsed


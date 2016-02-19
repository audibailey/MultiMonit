import yaml

fname = "config.yml"

def mkconfig(urls):
    with open(fname, "w") as f:
        yaml.dump({"URLS": urls, "refresh": 20}, f)

def readconfig():
    try:
        with open(fname) as f:
            data = yaml.load(f)

        return data
    except:
        return 0

def updateconfig(urls, refresh):
    with open(fname, "w") as f:
        yaml.dump({"URLS": urls, "refresh": refresh}, f)
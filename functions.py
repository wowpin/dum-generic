import time
import os

# Function for returning a first available key value for appending a new element to a dictionary
def getFreeKey(itemsDict):
    try:
        for x in range(0, len(itemsDict) + 1):
            if len(itemsDict[x]) > 0:
                pass
    except Exception:
        pass
    return(x)

# Function used for loggin messages to stdout and a disk file
def log(content, type):
    logfile = 'dum.log'
    print(str(time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + " [" + type + "] " + content))
    if os.path.exists(logfile):
        log = open(logfile, 'a')
    else:
        log = open(logfile, 'w')
    log.write(str(time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + " [" + type + "] " + content) + '\n')
    log.close()

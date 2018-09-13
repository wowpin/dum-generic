import time

# Function for returning a first available key value for appending a new element to a dictionary
def getFreeKey(itemsDict):
    try:
        for x in range(0, len(itemsDict) + 1):
            if len(itemsDict[x]) > 0:
                pass
    except Exception:
        pass
    return(x)
	
def log(content, type):
	print(str(time.strftime("%d/%m/%Y") + " " + time.strftime("%I:%M:%S") + " [" + type + "] " + content))

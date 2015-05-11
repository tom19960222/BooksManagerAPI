import time, datetime
def log(msg):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("%s: %s" % (time, msg))

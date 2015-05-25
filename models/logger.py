import time, datetime
def log(msg):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logfilename = datetime.datetime.now().strftime("%Y-%m-%d")
    logfile = open("%s.log" % (logfilename), 'a')
    logfile.write("%s: %s\n" % (time, msg))
    print("%s: %s" % (time, msg))

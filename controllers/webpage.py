from flask import Blueprint, render_template
import os, datetime

logpage = Blueprint('logpage', __name__, url_prefix='/log')

@logpage.route('')
def testpage():
    logtime = datetime.datetime.now().strftime("%Y-%m-%d")
    logfile = open(logtime+'.log', 'r')
    logcontent = list()
    for line in logfile:
        logcontent.append(line)
    logcontent.reverse()
    return render_template('log.html', title='Logfile '+logtime, logcontent=logcontent)

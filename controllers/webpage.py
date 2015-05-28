from flask import Blueprint, render_template, flash
import datetime

logpage = Blueprint('logpage', __name__, url_prefix='/log')

@logpage.route('', methods=['GET'])
def testpage():
    logtime = datetime.datetime.now().strftime("%Y-%m-%d")
    logfile = open(logtime+'.log', 'r')
    logcontent = list()
    for line in logfile:
        logcontent.append(line)
    logcontent.reverse()
    return render_template('log.html', title='Logfile '+logtime, logcontent=logcontent)

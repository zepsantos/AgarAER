from datetime import datetime


def generateTimestamp():
    now = datetime.now()
    return now


def getTimeStampDifMilis(last):
    now = generateTimestamp()
    dif = now-last
    return dif.microseconds
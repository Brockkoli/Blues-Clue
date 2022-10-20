import os
import datetime
import time
from random import randrange

# To generate a number from range
def generateNumber(rangeStart, rangeEnd):
    return randrange(rangeStart, rangeEnd)

def generateDay(month):
    if month == 1 or 3 or 5 or 7 or 8 or 10 or 12:
        return generateNumber(1, 31)
    elif month == 2:
        return generateNumber(1, 28)
    else:
        return generateNumber(1, 30)

def getDateTime(path):
    # File modification datetime
    modified_timestamp = os.path.getmtime(path)

    # Convert timestamp into DateTime object
    modifiedDT = datetime.datetime.fromtimestamp(modified_timestamp)
    print('Modified DateTime: ', modifiedDT)

    # # File creation datetime
    created_timestamp = os.path.getctime(path)

    # Convert timestamp into DateTime object
    createdDT = datetime.datetime.fromtimestamp(created_timestamp)
    print('Created DateTime: ', createdDT)

path = r"./Test.txt"

getDateTime(path)
generatedYear = generateNumber(2020, 2022)
generatedMonth = generateNumber(1, 12)
generatedDay = generateDay(generatedMonth)
generatedHour = generateNumber(00, 23)
generatedMinute = generateNumber(00, 59)
generatedSecond = generateNumber(0, 60)
generateMicrosecond = generateNumber(000000, 999999)

newDate = datetime.date

newDate = datetime.datetime(year=generatedYear, month=generatedMonth, day=generatedDay, hour=generatedHour, minute=generatedMinute, 
second=generatedSecond, microsecond=generateMicrosecond)
newModDate = time.mktime(newDate.timetuple())

os.utime(path, (newModDate, newModDate))
getDateTime(path)
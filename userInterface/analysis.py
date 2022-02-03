import dataCollection
import sendemail
import threading
from threading import Timer
import time
import datetime
import sqlite3

USER_EMAIL = ['jyl49@cam.ac.uk'] # ['abc@xyz.com','efg@xyz.com']
    
def time_in_range(current):
    """Returns whether current is in the range [start, end]"""
    start = datetime.time(8, 0, 0)
    end = datetime.time(17, 0, 0)
    if start <= end:
        return start <= current <= end
    else:
        return start <= current or current <= end
    
def schedule_db_timing():
    x = datetime.datetime.today()
    y = x.replace(day=x.day, hour=9, minute=00, second=0, microsecond=0) + datetime.timedelta(days=1)#daily
    delta_t = y - x
    secs = delta_t.total_seconds()
    return secs

def analyseMeasureAverage(TRIG,ECHO):
    read = 0
    read = dataCollection.measureAverage(TRIG,ECHO)
    if read > 900:
        avg_dist = 'Check connection'
    elif read > 80:
        avg_dist = 0
    elif read > 60:
        avg_dist = 0.25
    elif read > 40:
        avg_dist = 0.5
    else:
        avg_dist = 1
    return avg_dist
 
def analyseMeasure(TRIG,ECHO):
    read = 0
    read = dataCollection.measure(TRIG,ECHO)
    if read > 900:
        distance = 'Check connection'
    elif read > 80:
        distance = 0
    elif read > 60:
        distance = 0.25
    elif read > 40:
        distance = 0.5
    else:
        distance = 1
    return distance

def dataStorage():
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("stock_db.db")

    cur = con.cursor()

    # Return all results of query
    cur.execute('SELECT itemCode,remainStock,remainStockTrigger FROM barrels')
    result = cur.fetchall()

    # Be sure to close the connection
    con.close()
    return result

def schedule_db():
#     print('test')
    x = datetime.datetime.today()
    time_in = time_in_range (datetime.datetime.now().time())
    read1 = analyseMeasureAverage(7,11)
    read2 = analyseMeasureAverage(7,11)
    read3 = analyseMeasureAverage(7,11)
    read4 = analyseMeasureAverage(7,11)
    readings = [read1,read2,read3,read4]
#     print(readings)
    for i in range(len(readings)):
        if readings[i] == 0 and x.isoweekday() < 6 and time_in == True:
            sender = sendemail.Emailer()
            sendTo = USER_EMAIL
            emailSubject = "Liquid level is running low at Sensor "+str(i+1)
            emailContent = "Please ignore if not relevant to you. "
            sender.sendmail(sendTo, emailSubject, emailContent)
    result = dataStorage()
#     print(result)
    for i in range(len(result)) and x.isoweekday() < 6 and time_in == True:
        if result[i][1] == result[i][2]:
            sender = sendemail.Emailer()
            sendTo = USER_EMAIL
            emailSubject = "Remaining stock trigger for "+ result[i][0]
            emailContent = "Please ignore if not relevant to you. "
            sender.sendmail(sendTo, emailSubject, emailContent)        
    secs2 = schedule_db_timing()
#     print('secs2',secs2)
    Timer(secs2,schedule_db).start()#86400seconds=24hours
    
secs1 = schedule_db_timing()
# print('secs1',secs1)
t=Timer(secs1, schedule_db)
t.start()
time.sleep(0.1)

if __name__ == '__main__':
    g=dataCollection.measureAverage(7,11)
    print(g)
    h= analyseMeasureAverage(7,11)
    print(h)

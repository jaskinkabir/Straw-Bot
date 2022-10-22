import datetime
import math
import time



class log:
    def __init__(self, *name):
        self._enabled=True
        if len(name)>0:
            name=name[0]+'-'
        else:
            name=''
        now=datetime.datetime.now() #Create the log file
        self.logname=(f"{name}log_{now.month}-{now.day}-{now.year}__{now.hour}-{now.minute}-{now.second}")
    def log(self, message): #Logs message to log file and prints message to console
        if not self._enabled:
            print(message)
            return
        now=datetime.datetime.now()
        
        hour=now.hour
        minute=now.minute
        second=now.second
        
        if hour==0:#Pad single digit numbers
            hour="00"
        elif int(math.log(hour,10))==0:
            hour=f"0{now.hour}"
            
        if minute==0:
            minute="00"
        elif int(math.log(minute,10))==0:
            minute=f"0{now.minute}"
            
        if second==0:
            second="00"
        elif int(math.log(second,10))==0:
            second=f"0{second}"
            
        with open(f"logs/{self.logname}.txt","a+") as logfile:
            logfile.write(f"<{now.hour}:{now.minute}:{now.second}> {message}\n")#Write message with timestamp
            print(f"<{hour}:{minute}:{second}> {message}")#print message to console
    def disable(self):
        if self._enabled:
            self.log('log(): logging disabled')
            self._enabled=False
            
    def enable(self):
        if not self._enabled:
            self._enabled==True
            self.log('log(): logging enabled')

class runTimer:
    def __init__(self) -> None:
        pass
    def start(self):
        self._startTime=time.time()
    def end(self):
        self._endTime=time.time()
    def timeToFinish(self):
        return self._endTime-self._startTime
    def avgTimeToFinish(self, repetitions):
        timeSum=0
        for i in range(0,repetitions):
            timeSum+=self.timeToFinish()
        return timeSum/repetitions
    
def timeFunc(func, *args):
    start=time.time()
    func(*args)
    end=time.time()
    return end-start

def avgTimeFunc(repitions, func, *args):
    timeSum=0
    for i in range(0,repitions):
        timeSum+=timeFunc(func, *args)
    return timeSum/repitions
    
def textEnclosedParser(text, open, close):
    reading=False
    list=[]
    for char in text:
        if char==open: #Opening brace adds new message to list and starts reading characters
            list.append("")
            reading=True
            continue
        elif char==close: #Closing brace stops reading characters
            reading=False
            continue
        elif reading:
            list[-1]+=char
    return list
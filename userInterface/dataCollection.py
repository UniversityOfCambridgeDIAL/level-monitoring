
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
 
# TRIG = 7
# ECHO = 11
#  
# print ("Distance Measurement In Progress")
#  
# GPIO.setup(TRIG,GPIO.OUT)
# GPIO.setup(ECHO,GPIO.IN)
#  
# GPIO.output(TRIG, False)
# print ("Waiting For Sensor To Settle")
history=[]

total=0
count=0
distance=0
avg=0
dist=[]
distlist=[]
scan=False
maxTime = 0.04

def measureAverage(TRIG,ECHO):  
    history=[]

    starttime=time.time()
    for i in range(10):
        GPIO.setup(TRIG,GPIO.OUT)  
        GPIO.output(TRIG, False)
        time.sleep(0.1)
        #print("Waiting for sensor to settle...")
        #print("Please wait...")

        # ==========
        # GPIO Setup
        # ==========
        GPIO.output(TRIG, True)
        time.sleep(0.0001)
        GPIO.output(TRIG, False)
        GPIO.setup(ECHO,GPIO.IN)

        #print("Sending...")
        pulse_start=0
        pulse_end=0
        start=time.time()
        pulse_start=start
        while GPIO.input(ECHO)==0 and pulse_start-start<=0.00075:
            pulse_start=time.time()
        if round(pulse_start-start,3)>=0.300:
            print(timeout)
        else:
            #print("Receiving...")
            pulse_duration=0
            while GPIO.input(ECHO)==1 and pulse_duration<2:
                pulse_end=time.time()
                pulse_duration=pulse_end-pulse_start
                #print("Measuring...")
            
        pulse_duration=pulse_end-pulse_start

        # ====================
        # Calculating Distance
        # ====================
        distance=pulse_duration*17150
        distance=round(distance,2)
        if distance < 0:
            pass
        else:
            history.append(distance)
#         history.append(distance)
#         print(history)
    validcount=0
    total=0
#     print(history)
    for i in history:
        if i<150:
            validcount+=1
            total+=i
    if validcount>1:
        avg_dist=round(total/validcount,2)
#         print("Average distance:",avg_dist, "cm")
        return avg_dist
    else:
        return 999
#         if avg_dist<=50:
#             return([avg_dist,True,avg_dist,avg_dist])
#         else:
#             return([avg_dist,False,avg_dist,avg_dist])
#     else:
#         print("Timeout")
#         return([999,False,999,999]) 
 
def measure(TRIG,ECHO):
    pulse_duration = 0
    pulse_start = 0
    pulse_end = 0
    GPIO.setup(TRIG,GPIO.OUT)
     
    GPIO.output(TRIG, False)
    time.sleep(0.5)
    GPIO.output(TRIG, True)
    time.sleep(0.1)
    GPIO.output(TRIG, False)
    GPIO.setup(ECHO,GPIO.IN)

    pulse_start = time.time()
    timeout = pulse_start + maxTime
    while GPIO.input(ECHO)==0 and pulse_start < timeout:
        pulse_start = time.time()
        
#     pulse_end = time.time()
#     timeout = pulse_end + maxTime
    while GPIO.input(ECHO)==1 and pulse_duration < 2:#pulse_end < timeout:
        pulse_end = time.time()
        pulse_duration=pulse_end-pulse_start

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150

    distance = round(distance, 2)
    if distance < 0:
        distance = 999
#     print ("Distance:",distance,"cm")
    return distance
 
if __name__ == "__main__":
    loop = 1
    while loop == 1:
        x=measure(7,11) 
        y=measureAverage(15,15)#15,15
        print("measure:",x,", average:",y)
 
# GPIO.cleanup()
 
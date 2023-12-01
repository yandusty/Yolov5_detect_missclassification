import RPi.GPIO as GPIO 
import time 
import os

def speak(option, msg) :
    os.system("espeak {} '{}'".format(option,msg))

option = '-s 160'
msg = ['reset servo','number 1 servo','number 2 servo','number 3 servo','number 4 servo']
def servoMotor(pin, degree, t):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    pwm=GPIO.PWM(pin, 50)
    pwm.start(2)

    pwm.ChangeDutyCycle(degree)
    time.sleep(t)

    pwm.stop()
    GPIO.cleanup(pin)
while(True):
    N=int(input())
    if N==0:
        speak(option, msg[N])
        servoMotor(16, 2, 1)
        servoMotor(18, 2, 1)
        servoMotor(11, 2, 1)
        servoMotor(13, 2, 1)
        break
    elif N==1:
        speak(option, msg[N])
        servoMotor(16, 8, 1)
    elif N==2:
        speak(option, msg[N])
        servoMotor(18, 8, 1)
    elif N==3:
        speak(option, msg[N])
        servoMotor(11, 8, 1)
    elif N==4:
        speak(option, msg[N])
        servoMotor(13, 8, 1)

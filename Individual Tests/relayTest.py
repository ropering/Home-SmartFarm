import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(6,GPIO.OUT)  #열전구
GPIO.setup(13,GPIO.OUT) #생장LED
GPIO.setup(19,GPIO.OUT) #DC팬
GPIO.setup(26,GPIO.OUT) #워터펌프

print("setup")
time.sleep(2) #2초 쉬기

for i in range(1,3):
  GPIO.output(6,True)
  GPIO.output(13,True)
  GPIO.output(19,True)
  GPIO.output(26,True)
  print("true")
  time.sleep(2)

  GPIO.output(6,False) 
  GPIO.output(13,False)
  GPIO.output(19,False) 
  GPIO.output(26,False)
  print("false")
  time.sleep(2)

GPIO.cleanup() 
print("cleanup")
time.sleep(2)
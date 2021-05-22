'''
테스트 명 : 릴레이 개별 테스트(완료) -> 워터 펌프, 열 전구, 생장LED, DC팬 제어

날짜
  21.05.19
  
설명
  릴레이를 활용하여 높은 전압을 요구하는 하드웨어 제어
  
포트
  6 : 열전구
  13 : 생장LED
  19 : DC 팬
  26 : 워터 펌프
  
참고자료
  t.ly/yspt
'''
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

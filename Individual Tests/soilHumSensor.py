'''
테스트 명 : 토양습도 센서 개별 테스트(완료)

날짜
  21.05.19

설명
  측정 값 : 54(수분량 최대치) ~ 102(수분량 최저치)
  MCP3008 의 포트 1 사용
  MCP3008 : 디지털-아날로그 변환 모듈

포트
  추가 예정
  
참고자료
  t.ly/ItDS
  t.ly/egfT
'''

import RPi.GPIO as GPIO
import time
import spidev

GPIO.setmode(GPIO.BCM)
DIGIT = 23
GPIO.setup(DIGIT, GPIO.IN)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000


def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1, (8+adcChannel) << 4, 0])
    adcValue = ((buff[1] & 3) << 8)+buff[2]
    return adcValue

try:
  while True:
    adcValue = read_spi_adc(0)
    print("토양수분: %d "%(adcValue))
    digit_val=GPIO.input(DIGIT)
    print("Digit Value : %d"%(digit_val))
    time.sleep(0.5)
finally :
    GPIO.cleanup()
    spi.close()

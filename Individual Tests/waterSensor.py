'''
날짜
  21.05.19

설명
  작동되지만 0-3 범위 출력되는 코드
  MCP3008 의 포트 0 사용
  MCP3008 : 디지털-아날로그 변환 모듈

포트
  WATER_CHANNEL : 포트 번호

참고자료
  t.ly/lONP
'''
from typing import Mapping
import spidev
from time import sleep

spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 3
WATER_CHANNEL = 0

def readAnalog(channel):
  r = spi.xfer2([1, (8 + channel) << 4, 0])
  adc_out = ((r[1]&3) << 8) + r[2]
  return adc_out

while True:
  voltage = readAnalog(0) * 3.3/1024
  print(voltage)
  #statemachine.isWater=True
  sleep(1)


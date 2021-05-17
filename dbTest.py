'''
값 db 삽입 - db에서 값 가져와서 출력
'''
#스레딩 라이브러리
import threading
#온습도 라이브러리 #포트 4번
from method2 import *
import Adafruit_DHT as dht
from time import sleep
from flask import Flask, render_template, request
import sqlite3 as sql
import RPi.GPIO as GPIO
import spidev


#물 수위 입력
global vontage


#토양 수분 입력
def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1, (8+adcChannel) << 4, 0])
    adcValue = ((buff[1] & 3) << 8)+buff[2]
    return (adcValue/10)

adcValue = read_spi_adc(1) ## MCP3008포트, 원래 0 / 지금은 포트 1
# print("토양수분: %d "%(adcValue))
digit_val=GPIO.input(DIGIT)
# print("Digit Value : %d"%(digit_val))
    
while(True):
    voltage = (readAnalog(WATER_CHANNEL) * 3.3/1024) * 100
    tem, hum = getDHTdata()
    logDB(tem, hum, voltage, adcValue)
    print(returnDB())
    sleep(2)




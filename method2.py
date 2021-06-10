#온습도 라이브러리 #포트 4번
import Adafruit_DHT as dht
from time import sleep
from flask import Flask, render_template, request
import sqlite3 as sql
import RPi.GPIO as GPIO
import spidev

dbName = 'database.db'

def getDHTdata() :
    dhtPin = 4 #온습도 GPIO 포트
    global h
    global t
    h, t = dht.read_retry(dht.DHT11, dhtPin)
    h = round(h, 1) #소수점 둘째 자리에서 반올림
    t = round(t, 1)
    return t, h

def logDB(tem, hum, voltage, adcValue) :
    try :
            with sql.connect(dbName) as con :
                cur = con.cursor()
            # 온습도 값 DB 전송
            cur.execute('INSERT INTO STUDENTS (NAME, ADDR, CITY, PIN) VALUES (?,?,?,?)', (tem, hum, voltage, adcValue))
            con.commit() # 현재 행동 종료 느낌
            msg = 'Record successfully added'
    except :
            con.rollback() # 이전 값 유지,저장
            msg = 'Error in insert operation'
            print(msg)
    finally :
            con.close() 
            print(msg)

def returnDB() :
    try:
        with sql.connect(dbName) as con :
            cur = con.cursor()
        # DB 데이터 가져오기
        cur.execute('SELECT * FROM STUDENTS ORDER BY ROWID DESC LIMIT 1') #마지막 행 
        con.commit() 
        row = cur.fetchone()
        return row
    finally:
        cur.close()


# 물 수위 센서 (아날로그 0)
spi = spidev.SpiDev() #물 수위
spi.open(0,0)
spi.max_speed_hz = 1000000
spi.mode = 3
WATER_CHANNEL = 0

#물 수위 측정 함수
def readAnalog(channel):
  r = spi.xfer2([1, (8 + channel) << 4, 0])
  adc_out = ((r[1]&3) << 8) + r[2]
  return adc_out

# 토양 수분 관련 데이터
GPIO.setmode(GPIO.BCM)
DIGIT = 23 #GPIO 포트
GPIO.setup(DIGIT, GPIO.IN)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 50000

#토양 수분 입력
def read_spi_adc(adcChannel):
    adcValue = 0
    buff = spi.xfer2([1, (8+adcChannel) << 4, 0])
    adcValue = ((buff[1] & 3) << 8)+buff[2]
    return (adcValue/10)

def gpioSetting():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6,GPIO.OUT)  #열전구
    GPIO.setup(13,GPIO.OUT) #생장LED
    GPIO.setup(19,GPIO.OUT) #DC팬
    GPIO.setup(26,GPIO.OUT) #워터펌프
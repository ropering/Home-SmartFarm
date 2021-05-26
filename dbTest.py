'''
21.05.19
(온도, 습도, 수위 값, 토양수분 값) ---> db 저장 --->  db ---> html에 db값 출력 성공
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

gpioSetting()
heatBulb = 6
led = 13
fan = 19
waterPump = 26

global soilValue, waterValue, tem, hum, templateData
soilValue = 0.0
waterValue = 0.0
tem = 0.0
hum = 0.0

app = Flask(__name__)
#기본주소('/')로 들어오면
# route (URL에 웹페이지 연결하기)
@app.route('/')                   
def home():
    return render_template('index_04.html',  **templateData) #index.html에 전체 led현황을 함께 전달 

# Web에 display 클래스
class Thread1(threading.Thread):
    def run(self) :
        global soilValue, waterValue, tem, hum
        if __name__ == '__main__':
            app.run(debug=True, port=80, host='0.0.0.0', use_reloader = False)
# 센서값 → db → 변수에 저장
class Thread2(threading.Thread):
    def run(self):
        # 센서에서 값 받아오기
        while(True):
            print("thread3 시작")
            try:
                global soilValue, waterValue, tem, hum, templateData
                soilValue = read_spi_adc(1) ## MCP3008포트, 원래 0 / 지금은 포트 1
                waterValue = round((readAnalog(WATER_CHANNEL) * 3.3/1024) * 100, 1) # *100 은 일부러 값을 높인 것
                tem, hum = getDHTdata()

                with sql.connect(dbName) as con :
                    cur = con.cursor()
                # 데이터 db에 삽입  
                cur.execute('INSERT INTO STUDENTS (NAME, ADDR, CITY, PIN) VALUES (?,?,?,?)', (tem, hum, waterValue, soilValue))
                con.commit() 
                sleep(1)
                # DB 데이터 가져오기
                cur.execute('SELECT * FROM STUDENTS ORDER BY ROWID DESC LIMIT 1') #마지막 행 
                row = cur.fetchone()
                sleep(1)
                templateData = {
                    'temp' : row[0],
                    'hum' : row[1],
                    'water' : row[2],
                    'soil' : row[3]
                }
            finally:
                cur.close()
# 온도, 습도 -> 팬 작동, 중지
class Thread3(threading.Thread):
    def run(self) -> None:
        while(True):
            global soilValue, waterValue, tem, hum
            print(f'온도: {tem} 습도: {hum} 토양습도: {soilValue} 물 수위: {waterValue}')
            try:
                if tem > 20 or hum > 50:
                    print(f"팬이 작동 됩니다. 현재 온도: {tem} 현재 습도: {hum}")
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(fan,GPIO.OUT) #DC팬
                    GPIO.output(fan,True) 
                else:
                    print("팬이 중지 됩니다")
                    GPIO.output(heatBulb,False) 
            finally:
                GPIO.cleanup() 
            try:
                if tem < 15:
                    print(f"열전구가 작동 됩니다. 현재 온도: {tem}")
                    GPIO.setmode(GPIO.BCM)
                    GPIO.setup(heatBulb,GPIO.OUT) #열전구
                    GPIO.output(heatBulb,True) 
            finally:
                GPIO.cleanup() 
                    



# class Thread4(threading.Thread):
#     def run(self) -> None:
#         while(True):
#             global soilValue, waterValue, tem, hum
#             try:
#                 if tem < 15:
#                     print(f"열전구가 작동 됩니다. 현재 온도: {tem}")
#                     GPIO.setmode(GPIO.BCM)
#                     GPIO.setup(heatBulb,GPIO.OUT) #열전구
#                     GPIO.output(heatBulb,True) 
#                 else :
#                     print("열전구가 중지 됩니다")
#                     GPIO.output(heatBulb,False) 
#                     sleep(1)
#             finally:
#                 GPIO.cleanup() 
#             sleep(1)

# class Thread5(threading.Thread):
#     def run(self) -> None:
#         while(True):
#             global soilValue, waterValue, tem, hum
#             try:
#                 if soilValue > 100:
#                     print(f"모터, 팬이 작동 됩니다. 현재 토양습도: {soilValue}")
#                     GPIO.setmode(GPIO.BCM)
#                     GPIO.setup(waterPump,GPIO.OUT) #워터펌프
#                     GPIO.setup(fan,GPIO.OUT) #팬
#                     GPIO.output(waterPump,True) 
#                     GPIO.output(fan,True) 
#                 else :
#                     print("열전구가 중지 됩니다")
#                     GPIO.output(waterPump,False) 
#                     GPIO.output(fan,False) 
#                     sleep(1)
#             finally:
#                 GPIO.cleanup() 
#             sleep(1)

# class Thread6(threading.Thread):
#     def run(self) -> None:



t1 = Thread1()
t2 = Thread2()
t3 = Thread3()

t1.start()
t2.start()
t3.start()
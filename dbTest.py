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

dbName = 'database.db'

app = Flask(__name__)

@app.route('/')                   #기본주소('/')로 들어오면
def home():
    while(True) :
        # 센서에서 값 받아오기
        soilValue = read_spi_adc(1) ## MCP3008포트, 원래 0 / 지금은 포트 1
        waterValue = round((readAnalog(WATER_CHANNEL) * 3.3/1024) * 100, 1) # *100 은 일부러 값을 높인 것
        tem, hum = getDHTdata()

        try:
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
            return render_template('index_04.html',  temp = row[0], hum = row[1], water = row[2], soil = row[3]) #index.html에 전체 led현황을 함께 전달 
        finally:
            cur.close()

if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')



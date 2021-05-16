#온습도 라이브러리 #포트 4번
import Adafruit_DHT as dht
from time import sleep
from flask import Flask, render_template, request
import sqlite3 as sql

dbName = 'database.db'

def getDHTdata() :
    dhtPin = 4 #온습도 GPIO 포트
    global h
    global t
    h, t = dht.read_retry(dht.DHT22, dhtPin)
    h = round(h, 1)
    t = round(t, 1)
    return t, h

def logDB(tem, hum) :
    try :
            with sql.connect(dbName) as con :
                cur = con.cursor()
            # 온습도 값 DB 전송
            cur.execute('INSERT INTO STUDENTS (NAME, ADDR, CITY, PIN) VALUES (?,?,?,?)', (tem, hum, 3, 4))
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
'''
값 db 삽입 - db에서 값 가져와서 출력
'''

#온습도 라이브러리 #포트 4번
from method2 import *
import Adafruit_DHT as dht
from time import sleep
from flask import Flask, render_template, request
import sqlite3 as sql

dbName = 'database.db'


    
while(True):
    tem, hum = getDHTdata()
    logDB(tem, hum)
    print(returnDB())
    sleep(2)




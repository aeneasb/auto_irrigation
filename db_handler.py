import sqlite3
import queue 
import collections
import os
# This part has all functions to create and store values in a database.
# Generic structure of records
soil_moisture = collections.namedtuple('soil_moisture',['timestamp','voltage'])
water_level = collections.namedtuple('water_level',['timestamp','voltage'])
temperature = collections.namedtuple('temperature',['timestamp','voltage'])
light = collections.namedtuple('light',['timestamp','voltage'])
#Create sql table commands
SQL_CREATE_TABLE = '''
CREATE TABLE soil_moisture
(timestamp TEXT, 
soil_moisture INTEGER);
CREATE TABLE temperature
(timestamp TEXT,
temperature INTEGER);
CREATE TABLE light
(timestamp TEXT,
light INTEGER);
CREATE TABLE water_level
(timestamp TEXT,
water_level INTEGER);
'''
class Db_handler():
    def __init__(self,record_queue):
        self.record_queue = record_queue
    def create_db(self,db_path):
        sql_commands = SQL_CREATE_TABLE.split(';\n')
        self.conn = self.open_db(db_path)
        self.cursor = self.conn.cursor()
        for sql_command in sql_commands:
            self.cursor.execute(sql_command)
            self.conn.commit()
    def open_db(self,db_path):
        return sqlite3.connect(db_path)
    def open_or_create_db(self,db_path):
        if os.path.exists(db_path):
            self.conn = self.open_db(db_path)
            self.cursor = self.conn.cursor()
        else:
            self.create_db(db_path)
    def get_records(self):
        try:
            record = self.record_queue.get_nowait()
        except:
            return False
        if isinstance(record,soil_moisture):
            self.insert(record,'soil_moisture')
        if isinstance(record,light):
            self.insert(record,'light')
        if isinstance(record, water_level):
            self.insert(record,'water_level')
        if isinstance(record, temperature):
            self.insert(record, 'temperature')
    def insert(self,record,table):
        sql = 'INSERT INTO '+table+' VALUES (?, ?)'
        self.cursor.execute(sql, (str(record.timestamp),record.voltage))

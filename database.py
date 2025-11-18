"""
数据库操作模块
负责数据库连接、初始化和数据操作
"""

import sqlite3
from datetime import datetime
import config

class Database:
    def __init__(self):
        self.db_path = config.get_database_path()
        self.connection = None
        
    def connect(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute(config.DB_SCHEMA['users_table'])
        cursor.execute(config.DB_SCHEMA['attendance_table'])
        conn.commit()
        cursor.close()
        conn.close()
    
    def execute_query(self, query, params=None):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results
        finally:
            cursor.close()
            conn.close()
    
    def insert_user(self, username, password, email, role='employee'):
        conn = self.connect()
        cursor = conn.cursor()
        query = "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (username, password, email, role))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    
    def get_user_by_username(self, username):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    def get_user_by_id(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    
    def insert_attendance(self, user_id, check_in_time, check_out_time, date, status):
        conn = self.connect()
        cursor = conn.cursor()
        query = "INSERT INTO attendance (user_id, check_in_time, check_out_time, date, status) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (user_id, check_in_time, check_out_time, date, status))
        conn.commit()
        last_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return last_id
    
    def get_attendance_by_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM attendance WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    
    def get_attendance_by_date(self, user_id, date):
        conn = self.connect()
        cursor = conn.cursor()
        query = "SELECT * FROM attendance WHERE user_id = ? AND date = ?"
        cursor.execute(query, (user_id, date))
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        return records
    
    def update_checkout(self, attendance_id, check_out_time):
        conn = self.connect()
        cursor = conn.cursor()
        query = "UPDATE attendance SET check_out_time = ? WHERE id = ?"
        cursor.execute(query, (check_out_time, attendance_id))
        conn.commit()
        cursor.close()
        conn.close()
    
    def delete_user(self, user_id):
        conn = self.connect()
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
    
    def __del__(self):
        if self.connection:
            self.connection.close()

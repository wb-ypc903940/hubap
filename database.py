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
        """连接数据库"""
        self.connection = sqlite3.connect(self.db_path)
        return self.connection
    
    def init_database(self):
        """初始化数据库表"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(config.DB_SCHEMA['users_table'])
            cursor.execute(config.DB_SCHEMA['attendance_table'])
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    
    def execute_query(self, query, params=None):
        """执行查询(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
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
        """插入用户(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (username, password, email, role))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_username(self, username):
        """根据用户名获取用户(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            return user
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_id(self, user_id):
        """根据ID获取用户(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()
    
    def insert_attendance(self, user_id, check_in_time, check_out_time, date, status):
        """插入打卡记录(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "INSERT INTO attendance (user_id, check_in_time, check_out_time, date, status) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (user_id, check_in_time, check_out_time, date, status))
            conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
            conn.close()
    
    def get_attendance_by_user(self, user_id):
        """获取用户的打卡记录(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM attendance WHERE user_id = ?"
            cursor.execute(query, (user_id,))
            records = cursor.fetchall()
            return records
        finally:
            cursor.close()
            conn.close()
    
    def get_attendance_by_date(self, user_id, date):
        """获取指定日期的打卡记录(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM attendance WHERE user_id = ? AND date = ?"
            cursor.execute(query, (user_id, date))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    
    def update_checkout(self, attendance_id, check_out_time):
        """更新签退时间(参数化)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "UPDATE attendance SET check_out_time = ? WHERE id = ?"
            cursor.execute(query, (check_out_time, attendance_id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
    
    def delete_user(self, user_id):
        """删除用户(保持数据一致性由上层处理)"""
        conn = self.connect()
        try:
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

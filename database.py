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
        """连接数据库 - BUG: 资源未正确关闭"""
        self.connection = sqlite3.connect(self.db_path)
        # BUG: 没有异常处理
        return self.connection
    
    def init_database(self):
        """初始化数据库表"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # 创建用户表
        cursor.execute(config.DB_SCHEMA['users_table'])
        
        # 创建考勤表
        cursor.execute(config.DB_SCHEMA['attendance_table'])
        
        conn.commit()
        # BUG: 资源未关闭 - cursor和conn都没有close()
    
    def execute_query(self, query, params=None):
        """执行查询 - BUG: SQL注入漏洞"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # BUG: 直接使用字符串拼接，存在SQL注入风险
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        results = cursor.fetchall()
        # BUG: 没有关闭连接
        return results
    
    def insert_user(self, username, password, email, role='employee'):
        """插入用户 - BUG: SQL注入漏洞"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # BUG: 使用字符串格式化，存在严重SQL注入漏洞
        query = f"INSERT INTO users (username, password, email, role) VALUES ('{username}', '{password}', '{email}', '{role}')"
        cursor.execute(query)
        
        conn.commit()
        return cursor.lastrowid
        # BUG: 连接未关闭
    
    def get_user_by_username(self, username):
        """根据用户名获取用户"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # BUG: SQL注入漏洞 - 使用f-string拼接SQL
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        
        user = cursor.fetchone()
        conn.close()
        return user
    
    def get_user_by_id(self, user_id):
        """根据ID获取用户 - BUG: 空值检查缺失"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # BUG: 没有检查user_id是否为None或有效
        query = "SELECT * FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        
        return cursor.fetchone()
        # BUG: 连接未关闭
    
    def insert_attendance(self, user_id, check_in_time, check_out_time, date, status):
        """插入打卡记录"""
        conn = self.connect()
        cursor = conn.cursor()
        
        query = "INSERT INTO attendance (user_id, check_in_time, check_out_time, date, status) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (user_id, check_in_time, check_out_time, date, status))
        
        conn.commit()
        return cursor.lastrowid
    
    def get_attendance_by_user(self, user_id):
        """获取用户的打卡记录"""
        conn = self.connect()
        cursor = conn.cursor()
        
        query = "SELECT * FROM attendance WHERE user_id = ?"
        cursor.execute(query, (user_id,))
        
        records = cursor.fetchall()
        # BUG: 连接未关闭
        return records
    
    def get_attendance_by_date(self, user_id, date):
        """获取指定日期的打卡记录 - BUG: 逻辑错误"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # BUG: 使用了错误的列名进行查询
        query = f"SELECT * FROM attendance WHERE user_id = {user_id} AND date = '{date}'"
        cursor.execute(query)
        
        return cursor.fetchall()
    
    def update_checkout(self, attendance_id, check_out_time):
        """更新签退时间"""
        conn = self.connect()
        cursor = conn.cursor()
        
      # BUG: 缩进错误
        query = "UPDATE attendance SET check_out_time = ? WHERE id = ?"
        cursor.execute(query, (check_out_time, attendance_id))
        
        conn.commit()
        conn.close()
    
    def delete_user(self, user_id):
        """删除用户 - BUG: 数据一致性问题"""
        conn = self.connect()
        cursor = conn.cursor()
        
        # BUG: 删除用户时没有删除相关的打卡记录，违反数据一致性
        query = "DELETE FROM users WHERE id = ?"
        cursor.execute(query, (user_id,))
        
        conn.commit()
        conn.close()
    
    def __del__(self):
        """析构函数"""
        # BUG: 没有检查connection是否存在
        if self.connection:
            self.connection.close()

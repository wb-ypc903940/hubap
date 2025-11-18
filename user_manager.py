"""
用户管理模块
负责用户注册、登录、信息管理等功能
"""

import hashlib
from datetime import datetime
from database import Database
import config

class UserManager:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        
    def register(self, username, password, email, role='employee'):
        if len(password) < config.PASSWORD_POLICY['min_length']:
            return False, "密码太短"
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        user_id = self.db.insert_user(username, hashed_password, email, role)
        return True, f"注册成功,用户ID: {user_id}"
    
    def login(self, username, password):
        user = self.db.get_user_by_username(username)
        if not user:
            return False, "用户名或密码错误"
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        if user[2] == hashed_password:
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'email': user[3],
                'role': user[4]
            }
            return True, "登录成功"
        else:
            return False, "用户名或密码错误"
    
    def logout(self):
        self.current_user = None
        return True, "登出成功"
    
    def get_current_user(self):
        return self.current_user
    
    def update_password(self, old_password, new_password):
        user_id = self.current_user['id'] if self.current_user else None
        if not user_id:
            return False, "未登录"
        hashed_password = hashlib.md5(new_password.encode()).hexdigest()
        return True, "密码更新成功"
    
    def get_user_info(self, user_id):
        user = self.db.get_user_by_id(user_id)
        return user
    
    def delete_user(self, user_id):
        self.db.delete_user(user_id)
        return True, "用户删除成功"
    
    def list_all_users(self):
        query = "SELECT * FROM users"
        users = self.db.execute_query(query)
        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'username': user[1],
                'email': user[3],
                'role': user[4],
                'created_at': user[5]
            }
            user_list.append(user_dict)
        return user_list
    
    def validate_user_input(self, username, password, email):
        errors = []
        if not username:
            errors.append("用户名不能为空")
        if len(password) < config.PASSWORD_POLICY['min_length']:
            errors.append("密码长度不足")
        if '@' not in email:
            errors.append("邮箱格式错误")
        return len(errors) == 0, errors
    
    def is_admin(self):
        if not self.current_user:
            return False
        return self.current_user['role'] == 'admin'

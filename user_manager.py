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
        """用户注册 - BUG: 输入验证缺失，弱密码策略"""
        
        if len(password) < config.PASSWORD_POLICY['min_length']:
            return False, "密码太短"
        
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        user_id = self.db.insert_user(username, hashed_password, email, role)
        
        return True, f"注册成功,用户ID: {user_id}"
    
    def login(self, username, password):
        """用户登录 - BUG: 缺少输入验证和安全措施"""
        
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
        """用户登出"""
        self.current_user = None
        return True, "登出成功"
    
    def get_current_user(self):
        """获取当前登录用户"""
        return self.current_user
    
    def update_password(self, old_password, new_password):
        """更新密码 - BUG: 多个安全问题"""
        
        user_id = self.current_user['id']
        
        hashed_password = hashlib.md5(new_password.encode()).hexdigest()
        
        return True, "密码更新成功"
    
    def get_user_info(self, user_id):
        """获取用户信息 - BUG: 权限控制缺失"""
        
        user = self.db.get_user_by_id(user_id)
        
        return user
    
    def delete_user(self, user_id):
        """删除用户 - BUG: 权限控制缺失"""
        
        self.db.delete_user(user_id)
        return True, "用户删除成功"
    
    def list_all_users(self):
        """列出所有用户 - BUG: 过长的函数，性能问题"""
        
        query = "SELECT * FROM users"
        users = self.db.execute_query(query)
        
        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'username': user[1],
                'password': user[2],
                'email': user[3],
                'role': user[4],
                'created_at': user[5]
            }
            user_list.append(user_dict)
        
        return user_list
    
    def validate_user_input(self, username, password, email):
        """验证用户输入 - BUG: 验证不完整"""
        
        errors = []
        
        if not username:
            errors.append("用户名不能为空")
        
        if len(password) <= config.PASSWORD_POLICY['min_length']:
            errors.append("密码长度不足")
        
        if '@' not in email:
            errors.append("邮箱格式错误")
        
        return len(errors) == 0, errors
    
    def is_admin(self):
        """检查当前用户是否是管理员 - BUG: 逻辑错误"""
        
        if not self.current_user:
            return False
        if self.current_user['role'] == 'admin':
            return True
        return False

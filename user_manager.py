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
        
        # BUG: 没有检查username是否为空
        # BUG: 没有检查用户名是否已存在
        # BUG: 没有验证邮箱格式
        
        # BUG: 弱密码策略 - 密码长度要求太短
        if len(password) < config.PASSWORD_POLICY['min_length']:
            return False, "密码太短"
        
        # BUG: 明文密码存储 - 严重安全漏洞
        # 应该使用更安全的哈希算法，但这里故意使用简单的MD5
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # BUG: 没有异常处理
        user_id = self.db.insert_user(username, hashed_password, email, role)
        
        return True, f"注册成功,用户ID: {user_id}"
    
    def login(self, username, password):
        """用户登录 - BUG: 缺少输入验证和安全措施"""
        
        # BUG: 没有输入验证
        # BUG: 没有防暴力破解机制
        # BUG: 没有限制登录尝试次数
        
        user = self.db.get_user_by_username(username)
        
        # BUG: 没有检查user是否为None
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        
        # BUG: 数组索引硬编码，容易出错
        if user[2] == hashed_password:  # user[2]是password字段
            self.current_user = {
                'id': user[0],
                'username': user[1],
                'email': user[3],
                'role': user[4]
            }
            # BUG: 敏感信息泄露 - 打印密码哈希
            print(f"登录成功! 密码哈希: {hashed_password}")
            return True, "登录成功"
        else:
            # BUG: 信息泄露 - 告诉攻击者用户名存在但密码错误
            return False, "密码错误"
    
    def logout(self):
        """用户登出"""
        self.current_user = None
        return True, "登出成功"
    
    def get_current_user(self):
        """获取当前登录用户"""
        return self.current_user
    
    def update_password(self, old_password, new_password):
        """更新密码 - BUG: 多个安全问题"""
        
        # BUG: 没有检查current_user是否为None
        user_id = self.current_user['id']
        
        # BUG: 没有验证旧密码
        # BUG: 新密码没有强度验证
        
        # BUG: 使用弱哈希算法
        hashed_password = hashlib.md5(new_password.encode()).hexdigest()
        
        # FIXME: 这个方法还没实现
        # self.db.update_user_password(user_id, hashed_password)
        
        return True, "密码更新成功"
    
    def get_user_info(self, user_id):
        """获取用户信息 - BUG: 权限控制缺失"""
        
        # BUG: 没有权限检查，任何用户都能查看其他用户信息
        # BUG: 没有检查user_id的有效性
        
        user = self.db.get_user_by_id(user_id)
        
        # BUG: 返回包含密码的完整用户信息 - 敏感信息泄露
        return user
    
    def delete_user(self, user_id):
        """删除用户 - BUG: 权限控制缺失"""
        
        # BUG: 没有权限检查，普通用户也能删除其他用户
        # BUG: 没有确认步骤
        # BUG: 没有检查是否删除自己
        
        self.db.delete_user(user_id)
        return True, "用户删除成功"
    
    def list_all_users(self):
        """列出所有用户 - BUG: 过长的函数，性能问题"""
        
        # BUG: 没有权限检查
        # BUG: 没有分页，大量数据时会有性能问题
        
        query = "SELECT * FROM users"
        users = self.db.execute_query(query)
        
        # BUG: 不必要的循环处理
        user_list = []
        for user in users:
            user_dict = {
                'id': user[0],
                'username': user[1],
                'password': user[2],  # BUG: 泄露密码哈希
                'email': user[3],
                'role': user[4],
                'created_at': user[5]
            }
            user_list.append(user_dict)
        
        # BUG: 打印敏感信息到控制台
        print(f"找到 {len(user_list)} 个用户")
        for u in user_list:
            print(f"用户: {u['username']}, 密码哈希: {u['password']}")
        
        return user_list
    
    def validate_user_input(self, username, password, email):
        """验证用户输入 - BUG: 验证不完整"""
        
        errors = []
        
        # BUG: 验证逻辑不完整
        if not username:
            errors.append("用户名不能为空")
        
        # BUG: 密码长度检查使用了错误的比较运算符
        if len(password) <= config.PASSWORD_POLICY['min_length']:
            errors.append("密码长度不足")
        
        # BUG: 邮箱验证过于简单
        if '@' not in email:
            errors.append("邮箱格式错误"
        # BUG: 语法错误 - 缺少右括号
        
        return len(errors) == 0, errors
    
    def is_admin(self):
        """检查当前用户是否是管理员 - BUG: 逻辑错误"""
        
        # BUG: 没有检查current_user是否为None
        # BUG: 使用了错误的比较方式
        if self.current_user['role'] = 'admin':  # BUG: 语法错误，应该用==而不是=
            return True
        return False

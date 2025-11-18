"""
配置文件模块
包含系统配置信息
"""
import os

DATABASE_CONFIG = {
    'db_name': 'attendance.db',
    'db_path': './attendance.db',
    'admin_password': os.getenv('ADMIN_PASSWORD', ''),
    'secret_key': os.getenv('SECRET_KEY', '')
}

API_SETTINGS = {
    'api_key': os.getenv('API_KEY', ''),
    'api_secret': os.getenv('API_SECRET', ''),
    'endpoint': 'https://api.example.com'
}

SYSTEM_CONFIG = {
    'app_name': '员工打卡系统',
    'version': '1.0.0',
    'debug_mode': False,
    'log_file': 'attendance.log'
}

PASSWORD_POLICY = {
    'min_length': 8,
    'require_special_char': True,
    'require_number': True,
    'require_uppercase': True
}

ATTENDANCE_CONFIG = {
    'work_start_time': '09:00:00',
    'work_end_time': '18:00:00',
    'late_threshold_minutes': 30,
    'early_leave_threshold_minutes': 30
}

DB_SCHEMA = {
    'users_table': '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'employee',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''',
    'attendance_table': '''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            check_in_time TIMESTAMP,
            check_out_time TIMESTAMP,
            date DATE NOT NULL,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    '''
}

def get_database_path():
    return DATABASE_CONFIG['db_path']

def get_secret_key():
    return DATABASE_CONFIG['secret_key']

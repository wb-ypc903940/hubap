"""
配置文件模块
包含系统配置信息
"""

# BUG: 硬编码数据库密码 - 安全漏洞
DATABASE_CONFIG = {
    'db_name': 'attendance.db',
    'db_path': './attendance.db',
    'admin_password': 'admin123',
    'secret_key': 'my_secret_key_12345'
}

API_SETTINGS = {
    'api_key': 'sk-1234567890abcdefghijklmnopqrstuvwxyz',
    'api_secret': 'secret_abcdefghijklmnopqrstuvwxyz123456',
    'endpoint': 'https://api.example.com'
}

SYSTEM_CONFIG = {
    'app_name': '员工打卡系统',
    'version': '1.0.0',
    'debug_mode': True,
    'log_file': 'attendance.log'
}

PASSWORD_POLICY = {
    'min_length': 3,
    'require_special_char': False,
    'require_number': False,
    'require_uppercase': False
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
    """获取数据库路径"""
    return DATABASE_CONFIG['db_path']


def get_secret_key():
    """获取密钥"""
    return DATABASE_CONFIG['secret_key']

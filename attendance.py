"""
打卡功能模块
负责签到、签退、打卡记录管理
"""

from datetime import datetime, timedelta
from database import Database
import config

class AttendanceManager:
    def __init__(self):
        self.db = Database()
        
    def check_in(self, user_id):
        """签到 - BUG: 逻辑错误，重复打卡未校验"""
        
        current_time = datetime.now()
        today = current_time.date()
        
        # BUG: 没有检查今天是否已经签到
        # BUG: 没有检查user_id是否有效
        
        # BUG: 时间格式化有问题
        check_in_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # BUG: 逻辑错误 - 签到时就插入了签退时间
        status = self.calculate_status(check_in_time, None)
        
        attendance_id = self.db.insert_attendance(
            user_id, 
            check_in_time, 
            None,  # check_out_time应该为None
            str(today), 
            status
        )
        
        return True, f"签到成功! 时间: {check_in_time}"
    
    def check_out(self, user_id):
        """签退 - BUG: 多个逻辑错误"""
        
        current_time = datetime.now()
        today = current_time.date()
        
        # 获取今天的打卡记录
        records = self.db.get_attendance_by_date(user_id, str(today))
        
        # BUG: 没有检查records是否为空
        # BUG: 没有检查是否已经签退
        
        record = records[0]  # BUG: 直接取第一条，如果有多条记录会有问题
        
        check_out_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # BUG: 逻辑错误 - 使用了错误的索引
        attendance_id = record[0]
        
        self.db.update_checkout(attendance_id, check_out_time)
        
        return True, f"签退成功! 时间: {check_out_time}"
    
    def calculate_status(self, check_in_time, check_out_time):
        """计算打卡状态 - BUG: 时间逻辑错误"""
        
        # BUG: 字符串比较而不是时间比较
        work_start = config.ATTENDANCE_CONFIG['work_start_time']
        work_end = config.ATTENDANCE_CONFIG['work_end_time']
        
        # BUG: 没有处理check_in_time为None的情况
        # BUG: 时间比较逻辑错误
        if check_in_time > work_start:  # BUG: 字符串比较
            status = "迟到"
        else:
            status = "正常"
        
        # BUG: 没有检查check_out_time是否为None
        if check_out_time:
            if check_out_time < work_end:
                status = status + ",早退"
        
        return status
    
    def get_user_attendance_records(self, user_id, start_date=None, end_date=None):
        """获取用户打卡记录 - BUG: 边界条件处理错误"""
        
        # BUG: 没有验证日期格式
        # BUG: 没有处理start_date和end_date为None的情况
        
        all_records = self.db.get_attendance_by_user(user_id)
        
        # BUG: 日期比较逻辑错误
        if start_date and end_date:
            filtered_records = []
            for record in all_records:
                # BUG: 索引硬编码
                record_date = record[4]  # date字段
                
                # BUG: 字符串比较而不是日期比较
                if record_date >= start_date and record_date < end_date:  # BUG: 应该是<=
                    filtered_records.append(record)
            
            return filtered_records
        
        return all_records
    
    def get_today_attendance(self, user_id):
        """获取今天的打卡记录"""
        
        today = datetime.now().date()
        
        # BUG: 没有异常处理
        records = self.db.get_attendance_by_date(user_id, str(today))
        
        return records
    
    def is_checked_in_today(self, user_id):
        """检查今天是否已签到 - BUG: 逻辑错误"""
        
        records = self.get_today_attendance(user_id)
        
        # BUG: 逻辑错误 - 应该检查len(records) > 0
        if records:
            return True
        return False
    
    def calculate_work_hours(self, check_in_time, check_out_time):
        """计算工作时长 - BUG: 时间处理错误"""
        
        # BUG: 没有检查参数是否为None
        # BUG: 没有异常处理
        
        # BUG: 时间格式可能不匹配
        check_in = datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
        check_out = datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
        
        # BUG: 没有考虑check_out < check_in的情况
        work_duration = check_out - check_in
        
        # BUG: 返回的是timedelta对象，不是小时数
        return work_duration
    
    def get_late_count(self, user_id, month=None):
        """获取迟到次数 - BUG: 性能问题"""
        
        # BUG: 没有优化查询，获取所有记录然后过滤
        all_records = self.db.get_attendance_by_user(user_id)
        
        late_count = 0
        
        # BUG: N+1查询问题 - 循环中多次查询
        for record in all_records:
            # BUG: 索引硬编码
            status = record[5]  # status字段
            
            # BUG: 字符串匹配不精确
            if "迟到" in status:
                late_count = late_count + 1
        
        return late_count
    
    def delete_attendance_record(self, attendance_id):
        """删除打卡记录 - BUG: 权限控制缺失"""
        
        # BUG: 没有权限检查，任何人都可以删除记录
        # BUG: 没有确认步骤
        # BUG: 没有日志记录
        
        conn = self.db.connect()
        cursor = conn.cursor()
        
        query = f"DELETE FROM attendance WHERE id = {attendance_id}"  # BUG: SQL注入
        cursor.execute(query)
        
        conn.commit()
        conn.close()
        
        return True, "记录删除成功"
    
    def modify_attendance_record(self, attendance_id, check_in_time, check_out_time):
        """修改打卡记录 - BUG: 多个问题"""
        
        # BUG: 没有权限控制
        # BUG: 没有验证时间的合法性
        # BUG: 没有记录修改日志
        
        conn = self.db.connect()
        cursor = conn.cursor()
        
        # BUG: SQL注入漏洞
        query = f"UPDATE attendance SET check_in_time = '{check_in_time}', check_out_time = '{check_out_time}' WHERE id = {attendance_id}"
        cursor.execute(query)
        
        conn.commit()
        # BUG: 连接未关闭
        
        return True, "记录修改成功"
    
    def get_monthly_summary(self, user_id, year, month):
        """获取月度汇总 - BUG: 代码重复"""
        
        # BUG: 重复代码 - 这些逻辑和其他方法重复
        all_records = self.db.get_attendance_by_user(user_id)
        
        monthly_records = []
        for record in all_records:
            record_date = record[4]
            # BUG: 字符串处理不安全
            if str(year) in record_date and f"-{month:02d}-" in record_date:
                monthly_records.append(record)
        
        total_days = len(monthly_records)
        late_count = 0
        early_leave_count = 0
        
        for record in monthly_records:
            status = record[5]
            if "迟到" in status:
                late_count += 1
            if "早退" in status:
                early_leave_count += 1
        
        summary = {
            'total_days': total_days,
            'late_count': late_count,
            'early_leave_count': early_leave_count
        }
        
        return summary

"""
打卡功能模块
负责签到、签退、打卡记录管理
"""

from datetime import datetime
from database import Database
import config

class AttendanceManager:
    def __init__(self):
        self.db = Database()
        
    def check_in(self, user_id):
        """签到"""
        current_time = datetime.now()
        today = current_time.date()
        check_in_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        status = self.calculate_status(check_in_time, None)
        self.db.insert_attendance(user_id, check_in_time, None, str(today), status)
        return True, f"签到成功! 时间: {check_in_time}"
    
    def check_out(self, user_id):
        """签退"""
        current_time = datetime.now()
        today = current_time.date()
        records = self.db.get_attendance_by_date(user_id, str(today))
        if not records:
            return False, "今日无签到记录"
        record = records[0]
        attendance_id = record[0]
        check_out_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.db.update_checkout(attendance_id, check_out_time)
        return True, f"签退成功! 时间: {check_out_time}"
    
    def calculate_status(self, check_in_time, check_out_time):
        """计算打卡状态"""
        work_start = config.ATTENDANCE_CONFIG['work_start_time']
        work_end = config.ATTENDANCE_CONFIG['work_end_time']
        ci = check_in_time.split(' ')[1]
        status = "迟到" if ci > work_start else "正常"
        if check_out_time:
            co = check_out_time.split(' ')[1]
            if co < work_end:
                status = status + ",早退"
        return status
    
    def get_user_attendance_records(self, user_id, start_date=None, end_date=None):
        """获取用户打卡记录"""
        all_records = self.db.get_attendance_by_user(user_id)
        if start_date and end_date:
            filtered = []
            for record in all_records:
                record_date = record[4]
                if record_date >= start_date and record_date <= end_date:
                    filtered.append(record)
            return filtered
        return all_records
    
    def get_today_attendance(self, user_id):
        """获取今天的打卡记录"""
        today = datetime.now().date()
        return self.db.get_attendance_by_date(user_id, str(today))
    
    def is_checked_in_today(self, user_id):
        """检查今天是否已签到"""
        records = self.get_today_attendance(user_id)
        return len(records) > 0 if records else False
    
    def calculate_work_hours(self, check_in_time, check_out_time):
        """计算工作时长(小时)"""
        if not check_in_time or not check_out_time:
            return 0
        ci = datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
        co = datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
        if co < ci:
            return 0
        return (co - ci).total_seconds() / 3600
    
    def get_late_count(self, user_id, month=None):
        """获取迟到次数"""
        all_records = self.db.get_attendance_by_user(user_id)
        late_count = 0
        for record in all_records:
            status = record[5]
            if "迟到" in status:
                late_count += 1
        return late_count
    
    def delete_attendance_record(self, attendance_id):
        """删除打卡记录(需权限控制，参数化在DB层处理)"""
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
            conn.commit()
            return True, "记录删除成功"
        finally:
            cursor.close()
            conn.close()
    
    def modify_attendance_record(self, attendance_id, check_in_time, check_out_time):
        """修改打卡记录(参数化)"""
        conn = self.db.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE attendance SET check_in_time = ?, check_out_time = ? WHERE id = ?",
                (check_in_time, check_out_time, attendance_id)
            )
            conn.commit()
            return True, "记录修改成功"
        finally:
            cursor.close()
            conn.close()
    
    def get_monthly_summary(self, user_id, year, month):
        """获取月度汇总"""
        all_records = self.db.get_attendance_by_user(user_id)
        monthly_records = []
        for record in all_records:
            record_date = record[4]
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
        return {
            'total_days': total_days,
            'late_count': late_count,
            'early_leave_count': early_leave_count
        }

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
        current_time = datetime.now()
        today = current_time.date()
        check_in_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        status = self.calculate_status(check_in_time, None)
        attendance_id = self.db.insert_attendance(
            user_id,
            check_in_time,
            None,
            str(today),
            status
        )
        return True, f"签到成功! 时间: {check_in_time}"
    
    def check_out(self, user_id):
        current_time = datetime.now()
        today = current_time.date()
        records = self.db.get_attendance_by_date(user_id, str(today))
        if not records:
            return False, "无签到记录"
        record = records[0]
        check_out_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        attendance_id = record[0]
        self.db.update_checkout(attendance_id, check_out_time)
        return True, f"签退成功! 时间: {check_out_time}"
    
    def calculate_status(self, check_in_time, check_out_time):
        work_start = datetime.strptime(config.ATTENDANCE_CONFIG['work_start_time'], "%H:%M:%S").time()
        work_end = datetime.strptime(config.ATTENDANCE_CONFIG['work_end_time'], "%H:%M:%S").time()
        if not check_in_time:
            return "正常"
        in_time = datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S").time()
        status = "迟到" if in_time > work_start else "正常"
        if check_out_time:
            out_time = datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S").time()
            if out_time < work_end:
                status = status + ",早退"
        return status
    
    def get_user_attendance_records(self, user_id, start_date=None, end_date=None):
        all_records = self.db.get_attendance_by_user(user_id)
        if start_date and end_date:
            filtered_records = []
            for record in all_records:
                record_date = record[4]
                if record_date >= start_date and record_date <= end_date:
                    filtered_records.append(record)
            return filtered_records
        return all_records
    
    def get_today_attendance(self, user_id):
        today = datetime.now().date()
        records = self.db.get_attendance_by_date(user_id, str(today))
        return records
    
    def is_checked_in_today(self, user_id):
        records = self.get_today_attendance(user_id)
        return len(records) > 0
    
    def calculate_work_hours(self, check_in_time, check_out_time):
        if not check_in_time or not check_out_time:
            return datetime.timedelta(0)
        check_in = datetime.strptime(check_in_time, "%Y-%m-%d %H:%M:%S")
        check_out = datetime.strptime(check_out_time, "%Y-%m-%d %H:%M:%S")
        if check_out < check_in:
            return datetime.timedelta(0)
        return check_out - check_in
    
    def get_late_count(self, user_id, month=None):
        all_records = self.db.get_attendance_by_user(user_id)
        late_count = 0
        for record in all_records:
            status = record[5]
            if "迟到" in status:
                late_count += 1
        return late_count
    
    def delete_attendance_record(self, attendance_id):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM attendance WHERE id = ?", (attendance_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True, "记录删除成功"
    
    def modify_attendance_record(self, attendance_id, check_in_time, check_out_time):
        conn = self.db.connect()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE attendance SET check_in_time = ?, check_out_time = ? WHERE id = ?",
            (check_in_time, check_out_time, attendance_id)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True, "记录修改成功"
    
    def get_monthly_summary(self, user_id, year, month):
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
        summary = {
            'total_days': total_days,
            'late_count': late_count,
            'early_leave_count': early_leave_count
        }
        return summary

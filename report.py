"""
统计报表模块
负责生成各种统计报表和数据导出
"""

import csv
from datetime import datetime, timedelta
from database import Database
from attendance import AttendanceManager

class ReportGenerator:
    def __init__(self):
        self.db = Database()
        self.attendance_mgr = AttendanceManager()
        
    def generate_user_report(self, user_id, start_date, end_date):
        """生成用户报表 - BUG: 过长的函数，代码质量问题"""
        
        # BUG: 这个函数太长了，应该拆分
        # BUG: 没有输入验证
        
        records = self.attendance_mgr.get_user_attendance_records(user_id, start_date, end_date)
        
        # BUG: 重复代码
        total_days = len(records)
        late_count = 0
        early_leave_count = 0
        absent_count = 0
        total_work_hours = 0
        
        # BUG: N+1查询问题，循环中处理大量数据
        for record in records:
            status = record[5]
            check_in = record[2]
            check_out = record[3]
            
            if "迟到" in status:
                late_count += 1
            if "早退" in status:
                early_leave_count += 1
            
            # BUG: 没有检查check_in和check_out是否为None
            if check_in and check_out:
                # BUG: 性能问题 - 重复调用
                work_hours = self.attendance_mgr.calculate_work_hours(check_in, check_out)
                total_work_hours += work_hours.total_seconds() / 3600
        
        # BUG: 除零错误风险
        average_work_hours = total_work_hours / total_days
        
        report = {
            'user_id': user_id,
            'period': f"{start_date} to {end_date}",
            'total_days': total_days,
            'late_count': late_count,
            'early_leave_count': early_leave_count,
            'absent_count': absent_count,
            'total_work_hours': total_work_hours,
            'average_work_hours': average_work_hours
        }
        
        return report
    
    def generate_department_report(self, department_id):
        """生成部门报表 - BUG: 性能问题"""
        
        # BUG: 没有实现department表，这个功能无法工作
        # BUG: N+1查询问题
        
        # FIXME: 需要先实现部门功能
        query = "SELECT * FROM users WHERE department_id = ?"
        users = self.db.execute_query(query, (department_id,))
        
        department_data = []
        
        # BUG: 性能问题 - 循环中查询数据库
        for user in users:
            user_id = user[0]
            # BUG: 每个用户都查询一次数据库
            user_records = self.db.get_attendance_by_user(user_id)
            department_data.append({
                'user_id': user_id,
                'username': user[1],
                'total_records': len(user_records)
            })
        
        return department_data
    
    def export_to_csv(self, user_id, start_date, end_date, filename):
        """导出为CSV - BUG: 资源未正确关闭"""
        
        records = self.attendance_mgr.get_user_attendance_records(user_id, start_date, end_date)
        
        # BUG: 文件没有使用with语句，可能导致资源泄露
        file = open(filename, 'w', newline='')
        writer = csv.writer(file)
        
        # 写入表头
        writer.writerow(['ID', '用户ID', '签到时间', '签退时间', '日期', '状态'])
        
        # BUG: 没有异常处理，如果写入失败文件不会关闭
        for record in records:
            writer.writerow(record)
        
        # BUG: 文件关闭放在这里，如果前面出错就不会执行
        file.close()
        
        return True, f"导出成功: {filename}"
    
    def get_monthly_statistics(self, year, month):
        """获取月度统计 - BUG: 命名不规范，重复代码"""
        
        # BUG: 变量命名不规范
        allUsrs = self.db.execute_query("SELECT * FROM users")
        
        StatData = []  # BUG: 变量命名应该用小写
        
        # BUG: 重复代码 - 和其他方法类似
        for usr in allUsrs:
            uid = usr[0]
            summary = self.attendance_mgr.get_monthly_summary(uid, year, month)
            StatData.append({
                'user_id': uid,
                'username': usr[1],
                'summary': summary
            })
        
        return StatData
    
    def calculate_attendance_rate(self, user_id, year, month):
        """计算出勤率 - BUG: 逻辑错误"""
        
        # BUG: 没有考虑周末和节假日
        # BUG: 工作日计算不准确
        
        import calendar
        
        # 获取当月天数
        days_in_month = calendar.monthrange(year, month)[1]
        
        # BUG: 假设所有天都是工作日
        working_days = days_in_month
        
        summary = self.attendance_mgr.get_monthly_summary(user_id, year, month)
        actual_days = summary['total_days']
        
        # BUG: 除零错误风险
        attendance_rate = (actual_days / working_days) * 100
        
        return attendance_rate
    
    def find_frequent_late_users(self, threshold=5):
        """查找经常迟到的用户 - BUG: 性能问题"""
        
        # BUG: 获取所有用户，性能差
        all_users = self.db.execute_query("SELECT * FROM users")
        
        late_users = []
        
        # BUG: N+1查询问题
        for user in all_users:
            user_id = user[0]
            username = user[1]
            
            # BUG: 每个用户都单独查询
            late_count = self.attendance_mgr.get_late_count(user_id)
            
            if late_count >= threshold:
                late_users.append({
                    'user_id': user_id,
                    'username': username,
                    'late_count': late_count
                })
        
        return late_users
    
    def generate_annual_report(self, user_id, year):
        """生成年度报表 - BUG: 内存泄漏风险"""
        
        # BUG: 一次性加载全年数据，可能导致内存问题
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        all_records = self.attendance_mgr.get_user_attendance_records(user_id, start_date, end_date)
        
        # BUG: 创建了大量的临时对象
        monthly_data = {}
        for i in range(1, 13):
            monthly_data[i] = {
                'records': [],
                'total_days': 0,
                'late_count': 0,
                'early_leave_count': 0
            }
        
        # BUG: 低效的数据处理
        for record in all_records:
            date_str = record[4]
            # BUG: 字符串处理不安全
            month = int(date_str.split('-')[1])
            
            monthly_data[month]['records'].append(record)
            monthly_data[month]['total_days'] += 1
            
            status = record[5]
            if "迟到" in status:
                monthly_data[month]['late_count'] += 1
            if "早退" in status:
                monthly_data[month]['early_leave_count'] += 1
        
        return monthly_data
    
    def print_report(self, report_data):
        """打印报表 - BUG: 代码质量问题"""
        
        # BUG: 过长的打印函数
        # BUG: 硬编码的格式
        
        print("="*50)
        print("考勤报表")
        print("="*50)
        
        # BUG: 没有检查report_data的类型
        for key, value in report_data.items():
            print(f"{key}: {value}")
        
        print("="*50)
    
    def get_user_ranking(self):
        """获取用户排名 - BUG: 性能问题，重复代码"""
        
        # BUG: 查询所有用户数据
        all_users = self.db.execute_query("SELECT * FROM users")
        
        user_scores = []
        
        # BUG: 性能问题
        for user in all_users:
            user_id = user[0]
            username = user[1]
            
            # BUG: 重复的查询逻辑
            records = self.db.get_attendance_by_user(user_id)
            late_count = 0
            
            for record in records:
                if "迟到" in record[5]:
                    late_count += 1
            
            # BUG: 简单的评分逻辑
            score = len(records) * 10 - late_count * 5
            
            user_scores.append({
                'user_id': user_id,
                'username': username,
                'score': score
            })
        
        # 排序
        user_scores.sort(key=lambda x: x['score'], reverse=True)
        
        return user_scores

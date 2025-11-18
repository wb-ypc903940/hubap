"""
主程序入口
员工打卡系统主程序
"""

import sys
from database import Database
from user_manager import UserManager
from attendance import AttendanceManager
from report import ReportGenerator

class AttendanceSystem:
    def __init__(self):
        self.db = Database()
        self.user_mgr = UserManager()
        self.attendance_mgr = AttendanceManager()
        self.report_gen = ReportGenerator()
        
    def init_system(self):
        print("正在初始化数据库...")
        self.db.init_database()
        print("数据库初始化完成!")
        
    def show_menu(self):
        print("\n" + "="*50)
        print("欢迎使用员工打卡系统")
        print("="*50)
        print("1. 用户注册")
        print("2. 用户登录")
        print("3. 退出系统")
        print("="*50)
        
    def show_user_menu(self):
        print("\n" + "="*50)
        print("用户菜单")
        print("="*50)
        print("1. 签到")
        print("2. 签退")
        print("3. 查看我的打卡记录")
        print("4. 查看统计报表")
        print("5. 修改密码")
        print("6. 登出")
        print("="*50)
        
    def register(self):
        print("\n--- 用户注册 ---")
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        email = input("请输入邮箱: ")
        success, message = self.user_mgr.register(username, password, email)
        print(message)
        
    def login(self):
        print("\n--- 用户登录 ---")
        username = input("请输入用户名: ")
        password = input("请输入密码: ")
        success, message = self.user_mgr.login(username, password)
        print(message)
        if success:
            self.user_menu_loop()
        
    def check_in(self):
        user = self.user_mgr.get_current_user()
        user_id = user['id'] if user else None
        if not user_id:
            print("请先登录")
            return
        success, message = self.attendance_mgr.check_in(user_id)
        print(message)
        
    def check_out(self):
        user = self.user_mgr.get_current_user()
        user_id = user['id'] if user else None
        if not user_id:
            print("请先登录")
            return
        success, message = self.attendance_mgr.check_out(user_id)
        print(message)
        
    def view_my_records(self):
        user = self.user_mgr.get_current_user()
        user_id = user['id'] if user else None
        if not user_id:
            print("请先登录")
            return
        print("\n--- 我的打卡记录 ---")
        records = self.attendance_mgr.get_user_attendance_records(user_id)
        if not records:
            print("暂无记录")
            return
        for record in records:
            print(f"日期: {record[4]}, 签到: {record[2]}, 签退: {record[3]}, 状态: {record[5]}")
        
    def view_statistics(self):
        user = self.user_mgr.get_current_user()
        user_id = user['id'] if user else None
        if not user_id:
            print("请先登录")
            return
        print("\n--- 统计报表 ---")
        start_date = "2024-01-01"
        end_date = "2024-12-31"
        report = self.report_gen.generate_user_report(user_id, start_date, end_date)
        self.report_gen.print_report(report)
        
    def user_menu_loop(self):
        while True:
            self.show_user_menu()
            choice = input("\n请选择操作: ")
            if choice == "1":
                self.check_in()
            elif choice == "2":
                self.check_out()
            elif choice == "3":
                self.view_my_records()
            elif choice == "4":
                self.view_statistics()
            elif choice == "5":
                print("功能开发中...")
            elif choice == "6":
                self.user_mgr.logout()
                print("已登出")
                break
            else:
                print("无效的选择,请重新输入")
        
    def main_loop(self):
        while True:
            self.show_menu()
            choice = input("\n请选择操作: ")
            if choice == "1":
                self.register()
            elif choice == "2":
                self.login()
            elif choice == "3":
                print("感谢使用,再见!")
                sys.exit(0)
            else:
                print("无效的选择,请重新输入")

def main():
    system = AttendanceSystem()
    print("="*50)
    print("员工打卡系统 v1.0")
    print("="*50)
    system.init_system()
    system.main_loop()

if __name__ == "__main__":
    main()

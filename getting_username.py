import sqlite3 as sq
import tkinter as tk
from tkinter import messagebox

DB_PATH = "user_name.db"

class DBManager:
    def __init__ (self):
        self.conn = sq.connect(DB_PATH)
        self.cur = self.conn.cursor()
        self.setup()

    def setup(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY,password TEXT,role TEXT,fullname TEXT)")

    def register(self, u, p, role, fullname):
        try:
            self.cur.execute(
                "INSERT INTO users VALUES (?,?,?,?)",
                (u, p, role, fullname)
            )
            self.conn.commit()
            return True
        except:
            return False

    def login(self, u, p):
        self.cur.execute(
            "SELECT password,role,fullname FROM users WHERE username=?",
            (u,)
        )
        row = self.cur.fetchone()

        if row and row[0] == p:
            return row[1], row[2] 
        return None

#___________________با استفاده از هوش مصنوعی________________________________
class App:
    def __init__(self, root):
        self.db = DBManager()
        self.root = root
        self.root.title("سیستم جامع گروه رافا")
        self.root.geometry("300x400")
        
        # استایل ساده
        self.label_font = ("Arial", 10)
        
        self.main_frame()

    def main_frame(self):
        # پاک کردن فریم قبلی برای تغییر صفحات
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="خوش آمدید", font=("Arial", 14, "bold")).pack(pady=20)
        
        tk.Button(self.root, text="ورود به حساب", width=20, command=self.login_screen).pack(pady=10)
        tk.Button(self.root, text="ثبت‌نام کاربر جدید", width=20, command=self.register_screen).pack(pady=10)

    def login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="ورود", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(self.root, text="نام کاربری:").pack()
        u_entry = tk.Entry(self.root)
        u_entry.pack()

        tk.Label(self.root, text="رمز عبور:").pack()
        p_entry = tk.Entry(self.root, show="*") # برای مخفی شدن پسورد
        p_entry.pack()

        def attempt_login():
            user = u_entry.get()
            pw = p_entry.get()
            result = self.db.login(user, pw)
            if result:
                role, fullname = result
                messagebox.showinfo("موفقیت", f"خوش آمدید {fullname}!\nنقش شما: {role}")
            else:
                messagebox.showerror("خطا", "نام کاربری یا رمز عبور اشتباه است")

        tk.Button(self.root, text="ورود", command=attempt_login, bg="lightgreen").pack(pady=10)
        tk.Button(self.root, text="بازگشت", command=self.main_frame).pack()

    def register_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="ثبت‌نام", font=("Arial", 12, "bold")).pack(pady=10)

        fields = ["نام کاربری", "رمز عبور", "نقش (مثلا Admin)", "نام و نام خانوادگی"]
        entries = {}

        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack()
            entries[field] = entry

        def attempt_register():
            u = entries["نام کاربری"].get()
            p = entries["رمز عبور"].get()
            r = entries["نقش (مثلا Admin)"].get()
            f = entries["نام و نام خانوادگی"].get()

            if u and p and r and f:
                if self.db.register(u, p, r, f):
                    messagebox.showinfo("موفقیت", "کاربر با موفقیت ثبت شد")
                    self.main_frame()
                else:
                    messagebox.showerror("خطا", "نام کاربری تکراری است!")
            else:
                messagebox.showwarning("هشدار", "لطفاً همه فیلدها را پر کنید")

        tk.Button(self.root, text="ثبت‌نام", command=attempt_register, bg="lightblue").pack(pady=10)
        tk.Button(self.root, text="بازگشت", command=self.main_frame).pack()




if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
import tkinter as tk
import subprocess
from tkinter import scrolledtext, messagebox

def open_script_onetime():
    subprocess.Popen(['python', 'C:\\Users\\Benson\\Desktop\\BCP_CMD\\Main\\insert_onetime.py'])

def open_script_D_table_insert():
    subprocess.Popen(['python', 'C:\\Users\\Benson\\Desktop\\BCP_CMD\\Main\\D_table_insert.py'])

def open_script_CH_DATE():
    subprocess.Popen(['python', 'C:\\Users\\Benson\\Desktop\\BCP_CMD\\Main\\CH_DATE.py'])
    
def open_script_CH_encode():
    subprocess.Popen(['python', 'C:\\Users\\Benson\\Desktop\\BCP_CMD\\Main\\change_encode.py'])
    
# 創建主窗口
root = tk.Tk()
root.title("移轉SQL_Tool")

# 設置窗口大小
root.geometry("600x480")


# 創建按鈕並綁定到打開指定Python腳本的函數
button1 = tk.Button(root, text="導入onetime_PostgreSQL", command=open_script_onetime)
button1.pack(pady=10)

button2 = tk.Button(root, text="導入需要刪除table的資料", command=open_script_D_table_insert)
button2.pack(pady=10)

button3 = tk.Button(root, text="時間格式轉換", command=open_script_CH_DATE)
button3.pack(pady=10)

button4 = tk.Button(root, text="轉換編碼_UTF-8", command=open_script_CH_encode)
button4.pack(pady=10)


# 啟動主循環
root.mainloop()

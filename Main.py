import tkinter as tk
import subprocess
from tkinter import scrolledtext, messagebox


script_path = r'\\fs1\Tool\Benson\SQL_Tool'       
        
def open_script_onetime():
   
    process = subprocess.Popen(['python', script_path+'\insert_onetime.py'])

def open_script_D_table_insert():
    process =  subprocess.Popen(['python', script_path+'\D_table_insert.py'])

def open_script_CH_DATE():
    
    process =  subprocess.Popen(['python', script_path+'\CH_DATE.py'])
def open_script_CH_encode():
    process =  subprocess.Popen(['python', script_path+'\change_encode.py'])

def open_script_alter_column():
    process = subprocess.Popen(['python',   script_path+'\\alter_table.py'])

def open_script_single_insert():
    process = subprocess.Popen(['python',   script_path+'\single_insert.py'])
    

root = tk.Tk()
root.title("移轉SQL_Tool")


root.geometry("600x480")


button1 = tk.Button(root, text="導入onetime_PostgreSQL", command=open_script_onetime)
button1.pack(pady=10)

button2 = tk.Button(root, text="導入需要刪除table的資料", command=open_script_D_table_insert)
button2.pack(pady=10)

button3 = tk.Button(root, text="時間格式轉換", command=open_script_CH_DATE)
button3.pack(pady=10)

button4 = tk.Button(root, text="轉換編碼_UTF-8", command=open_script_CH_encode)
button4.pack(pady=10)

button5 = tk.Button(root,text="變更欄位Type",command=open_script_alter_column)
button5.pack(pady=10)

button6 = tk.Button(root,text="單項插入",command=open_script_single_insert)
button6.pack(pady=10)


root.mainloop()

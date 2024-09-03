import os
import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askdirectory
import subprocess

def run_script():
    conn_string = conn_string_entry.get()  # 获取用户输入的连接字符串
    if not conn_string:
        messagebox.showwarning("Warning", "请输入连接字符串")
        return
    
    # 跳出选单让用户选择CSV文件目录
    csv_directory = askdirectory(title='請選擇指定目錄')
    
    # 如果用户未选择目录，则退出函数
    if not csv_directory:
        print("未选择目錄")
        return

    imported_tables_file = os.path.join(csv_directory, 'imported_tables.txt')

    # 创建SQLAlchemy引擎
    engine = create_engine(conn_string)

    # 读取已导入的表名列表
    if os.path.exists(imported_tables_file):
        with open(imported_tables_file, 'r') as f:
            imported_tables = set(f.read().splitlines())
    else:
        imported_tables = set()

    # 遍历CSV文件目录中的文件
    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            table_name = os.path.splitext(file_name)[0]  
            
            # 跳过已导入的表
            if table_name in imported_tables:
                log_text.insert(tk.END, f"跳過 {table_name}\n")
                continue
            
            csv_file_path = os.path.join(csv_directory, file_name)
            
            # 读取CSV文件为DataFrame
            df = pd.read_csv(csv_file_path, sep='|')
            
            # 将DataFrame数据写入到PostgreSQL表中
            df.to_sql(table_name, engine, if_exists='append', index=False)
            log_text.insert(tk.END, f"已將文件 {file_name} 導入到 {table_name}\n")
            
            # 将表名添加到已导入列表并写入文件
            with open(imported_tables_file, 'a') as f:
                f.write(f"{table_name}\n")
            imported_tables.add(table_name)

    log_text.insert(tk.END, "所有文件均已成功導入到PostgreSQL\n")

# 初始化Tkinter主窗口
root = tk.Tk()
root.title("CSV to PostgreSQL Importer")
root.geometry("600x300")

# 创建一个标签和文本框，预填充连接字符串
tk.Label(root, text="Enter Connection String:").pack(pady=5)
conn_string_entry = tk.Entry(root, width=70)
conn_string_entry.pack(padx=10, pady=5)
conn_string_entry.insert(0, "postgresql://postgres:120129@localhost:5432/Romis")  # 预填充文本框

# 创建一个按钮，点击按钮时执行Python脚本
run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=10)

# 创建一个文本框，显示脚本的日志和输出
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
log_text.pack(padx=10, pady=10)

# 运行Tkinter主循环
root.mainloop()

import os
import pandas as pd
from sqlalchemy import create_engine, text
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askdirectory

def run_script():
    conn_string = conn_string_entry.get()  # 获取用户输入的连接字符串
    if not conn_string:
        messagebox.showwarning("Warning", "请输入連接字串")
        return
    
    # 跳出选单让用户选择CSV文件目录
    csv_directory = askdirectory(title='請選擇指定目錄')
    
    # 如果用户未选择目录，则退出函数
    if not csv_directory:
        log_text.insert(tk.END, "未选择目錄\n")
        log_text.update()  # 刷新文本框
        return
    
    engine = create_engine(conn_string)
    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            table_name = os.path.splitext(file_name)[0]  # 从文件名获取表名
            csv_file_path = os.path.join(csv_directory, file_name)
        
            # 删除已有的表
            try:
                with engine.connect() as connection:
                    connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
                    log_text.insert(tk.END, f"已删除表 {table_name}\n")
                    log_text.update()  # 刷新文本框
                
                # 读取CSV文件为DataFrame
                df = pd.read_csv(csv_file_path, sep='|')
            
                # 将DataFrame数据写入到PostgreSQL表中
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                log_text.insert(tk.END, f"已將文件 {file_name} 導入到 {table_name}\n")
                log_text.update()  # 刷新文本框
            except Exception as e:
                log_text.insert(tk.END, f"错误: {e}\n")
                log_text.update()  # 刷新文本框

    log_text.insert(tk.END, "所有文件均已成功導入到PostgreSQL\n")
    log_text.update()  # 刷新文本框

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

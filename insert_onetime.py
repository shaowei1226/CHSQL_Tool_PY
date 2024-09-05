import os
import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askdirectory
import subprocess

def run_script():
    conn_string = conn_string_entry.get()  
    if not conn_string:
        messagebox.showwarning("Warning", "請輸入連接字串")
        return
    
    
    csv_directory = askdirectory(title='請選擇指定目錄')
    
  
    if not csv_directory:
        print("未選擇目錄")
        return

    imported_tables_file = os.path.join(csv_directory, 'imported_tables.txt')

    
    engine = create_engine(conn_string)

    
    if os.path.exists(imported_tables_file):
        with open(imported_tables_file, 'r') as f:
            imported_tables = set(f.read().splitlines())
    else:
        imported_tables = set()

    
    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            table_name = os.path.splitext(file_name)[0]  
            
            
            if table_name in imported_tables:
                log_text.insert(tk.END, f"跳過 {table_name}\n")
                continue
            
            csv_file_path = os.path.join(csv_directory, file_name)
            
           
            df = pd.read_csv(csv_file_path, sep='|')
            
            
            df.to_sql(table_name, engine, if_exists='append', index=False)
            log_text.insert(tk.END, f"已將文件 {file_name} 導入到 {table_name}\n")
            
            
            with open(imported_tables_file, 'a') as f:
                f.write(f"{table_name}\n")
            imported_tables.add(table_name)

    log_text.insert(tk.END, "所有文件均已成功導入到PostgreSQL\n")


root = tk.Tk()
root.title("CSV to PostgreSQL Importer")
root.geometry("600x300")


tk.Label(root, text="Enter Connection String:").pack(pady=5)
conn_string_entry = tk.Entry(root, width=70)
conn_string_entry.pack(padx=10, pady=5)
conn_string_entry.insert(0, "postgresql://postgres:120129@localhost:5432/Romis")  # 预填充文本框


run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=10)


log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
log_text.pack(padx=10, pady=10)


root.mainloop()

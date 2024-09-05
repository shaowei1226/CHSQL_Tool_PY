import os
import pandas as pd
from sqlalchemy import create_engine, text
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askdirectory

def run_script():
    conn_string = conn_string_entry.get()  
    if not conn_string:
        messagebox.showwarning("Warning", "請輸入連接字串")
        return
    

    csv_directory = askdirectory(title='請選擇指定目錄')
    
    
    if not csv_directory:
        log_text.insert(tk.END, "未選取目錄\n")
        log_text.update()
        return
    
    engine = create_engine(conn_string)
    for file_name in os.listdir(csv_directory):
        if file_name.endswith('.csv'):
            table_name = os.path.splitext(file_name)[0]  
            csv_file_path = os.path.join(csv_directory, file_name)
        
            # 删除已有的table
            try:
                with engine.connect() as connection:
                    connection.execute(text(f"DROP TABLE IF EXISTS {table_name};"))
                    log_text.insert(tk.END, f"已删除 {table_name}\n")
                    log_text.update()  
                
                # 設定CSV文件為DataFrame,SEP='|'分隔符號
                df = pd.read_csv(csv_file_path, sep='|')
            
                # 將DataFrame寫入到PostgreSQL
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                log_text.insert(tk.END, f"已將文件 {file_name} 導入到 {table_name}\n")
                log_text.update()  
            except Exception as e:
                log_text.insert(tk.END, f"Error: {e}\n")
                log_text.update()  

    log_text.insert(tk.END, "所有文件均已成功導入到PostgreSQL\n")
    log_text.update() #刷新LOG

root = tk.Tk()
root.title("CSV to PostgreSQL Importer")
root.geometry("600x300")


tk.Label(root, text="Enter Connection String:").pack(pady=5)
conn_string_entry = tk.Entry(root, width=70)
conn_string_entry.pack(padx=10, pady=5)
conn_string_entry.insert(0, "postgresql://postgres:120129@localhost:5432/Romis")


run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.pack(pady=10)

log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
log_text.pack(padx=10, pady=10)


root.mainloop()

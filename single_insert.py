import os
import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askopenfilename

def run_script():
    conn_string = conn_string_entry.get()  
    if not conn_string:
        messagebox.showwarning("Warning", "請輸入連接字串")
        return
    

    csv_file_path = askopenfilename(title='請選擇CSV文件', filetypes=[('CSV files', '*.csv')])
    
    
    if not csv_file_path:
        print("未選擇文件")
        return


    engine = create_engine(conn_string)

    
    file_name = os.path.basename(csv_file_path)
    table_name = os.path.splitext(file_name)[0]  
    
   
    df = pd.read_csv(csv_file_path, sep='|')
    
   
    df.to_sql(table_name, engine, if_exists='append', index=False)
    log_text.insert(tk.END, f"已將文件 {file_name} 導入到 {table_name}\n")


root = tk.Tk()
root.title("CSV to PostgreSQL")
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
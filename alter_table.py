import os
import pandas as pd
from sqlalchemy import create_engine
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askdirectory
import subprocess
from sqlalchemy.sql import text

def run_script():
    conn_string = conn_string_entry.get()
    engine = create_engine(conn_string)
    table_name = table_entry.get()
    column_name = column_entry.get()
    new_type = Type_entry.get()
    
    #postgresql語法
    alter_query = f"ALTER TABLE {table_name} ALTER COLUMN {column_name} TYPE {new_type};"
    #log_text.insert(tk.END, f"Executing query: {alter_query}\n")
    
    try:
        with engine.connect() as connection:
            connection.execute(text(alter_query))
        log_text.insert(tk.END, f"Successfully changed {table_name} column {column_name} to {new_type}.\n")
    except Exception as e:
        log_text.insert(tk.END, f"Error: {str(e)}\n")

   

root = tk.Tk()
root.title("Alter table")
root.geometry("600x300")


tk.Label(root, text="Enter Connection String:").pack(pady=5)
conn_string_entry = tk.Entry(root, width=70)
conn_string_entry.pack(padx=10, pady=5)
conn_string_entry.insert(0, "postgresql://postgres:120129@localhost:5432/Romis")  

tk.Label(root,text="Table").place(x=10,y=60)
table_entry = tk.Entry(root, width=20)
table_entry.place(x=10, y=80)
tk.Label(root,text="Column").place(x=10,y=100)
column_entry = tk.Entry(root, width=20)
column_entry.place(x=10, y=120)
tk.Label(root,text="Type").place(x=10,y=140)
Type_entry = tk.Entry(root, width=20)
Type_entry.place(x=10, y=160)




run_button = tk.Button(root, text="Run Script", command=run_script)
run_button.place(x=10,y=200)


log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=50)
log_text.place(x=180, y=80)


root.mainloop()

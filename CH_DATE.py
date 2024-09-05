import os
import pandas as pd
from datetime import datetime
from tkinter.filedialog import askdirectory
import tkinter as tk


   

csv_directory = askdirectory(title='請選擇指定目錄')
    
  
if not csv_directory:
    print("未選擇目錄")
    
    
LOG_FILE = 'processed_log.txt'

def read_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logged_files = {line.strip() for line in f}
        return logged_files
    return set()

def write_log(file_name):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{file_name}\n")

# 轉換日期時間格式
def convert_datetime_format(date_str):
    try:
       
        date_obj = datetime.strptime(date_str, '%b %d %Y %I:%M:%S:%f%p')
        # 格式化為指定的日期時間格式
        return date_obj.strftime('%Y/%m/%d %H:%M:%S')
    except ValueError:
        return date_str  
    except TypeError:
        return date_str  

processed_files = read_log()


for filename in os.listdir(csv_directory):
    if filename.endswith('.csv'):
        if filename in processed_files:
            print(f"Skipping {filename}: Already processed.")
            continue            
            
            
           
        file_path = os.path.join(csv_directory, filename)
        try:
            
            df = pd.read_csv(file_path, encoding='utf-8', on_bad_lines='skip', sep='|')
            
            df = df.applymap(convert_datetime_format)
            
            
            df.to_csv(file_path, index=False, sep='|')
            
            print(f'{filename} 處理完成')
            
            write_log(filename)

        except pd.errors.ParserError as e:
            print(f'處理 {filename} 時發生錯誤: {e}')

    print("所有檔案處理完成！")


root = tk.Tk()
root.title("Time")
root.geometry("600x300")



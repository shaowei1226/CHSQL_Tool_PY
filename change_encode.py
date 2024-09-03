import os
import chardet
import tkinter as tk
from tkinter import scrolledtext, messagebox
from tkinter.filedialog import askdirectory

LOG_FILE = 'encode_log.txt'

def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result.get('encoding')

def convert_encoding(input_file, output_file, from_encoding, to_encoding='utf-8'):
    with open(input_file, 'r', encoding=from_encoding, errors='ignore') as f:
        content = f.read()

    with open(output_file, 'w', encoding=to_encoding) as f:
        f.write(content)

def read_log():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            logged_files = {line.strip() for line in f}
        return logged_files
    return set()

def write_log(file_name):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{file_name}\n")

def process_files():
    folder_path = askdirectory(title='請選擇指定目錄')
    
    if not folder_path:
        messagebox.showwarning("Warning", "未選擇目錄")
        return
    
    processed_files = read_log()
    log_text.delete(1.0, tk.END)
    
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path) and file_name.endswith('.csv'):
            if file_name in processed_files:
                log_text.insert(tk.END, f"Skipping {file_name}: Already processed.\n")
                continue

            encoding = detect_encoding(file_path)
            if encoding is None:
                log_text.insert(tk.END, f"Skipping {file_name}: Unable to detect encoding.\n")
                write_log(file_name)
                continue
            
            encoding = encoding.lower()
            if encoding == 'big5':
                log_text.insert(tk.END, f"Converting {file_name} from BIG5 to UTF-8\n")
                convert_encoding(file_path, file_path, from_encoding='big5')
            elif encoding == 'iso-8859-1':
                log_text.insert(tk.END, f"Converting {file_name} from ISO-8859-1 to UTF-8\n")
                convert_encoding(file_path, file_path, from_encoding='ISO-8859-1')
            elif encoding == 'gb2312':
                log_text.insert(tk.END, f"Converting {file_name} from GB2312 to UTF-8\n")
                convert_encoding(file_path, file_path, from_encoding='GB2312')
            elif encoding == 'utf-8':
                log_text.insert(tk.END, f"{file_name} is already UTF-8\n")
            else:
                log_text.insert(tk.END, f"{file_name} is in {encoding} encoding, no conversion done.\n")

            write_log(file_name)  
    log_text.insert(tk.END, "所有檔案處理完成！\n")

root = tk.Tk()
root.title("CSV Encoding Converter")
root.geometry("600x400")

# Button to start the file processing
run_button = tk.Button(root, text="Process Files", command=process_files)
run_button.pack(pady=10)

# ScrolledText to display the log
log_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=15, width=70)
log_text.pack(padx=10, pady=10)

# Run the Tkinter main loop
root.mainloop()

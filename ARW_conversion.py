# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 22:56:02 2023

@author: User
"""

import tkinter as tk
from tkinter.constants import CENTER
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import os 
import rawpy
import imageio
import threading
import time

## ========================== close button ===============================
def close_window():
    window.destroy()

## ============================ choose folder =============================
def choose_ARW_folder():
    global ARW_folder
    ARW_folder = filedialog.askdirectory()
    path1.set(ARW_folder)

def choose_save_folder():
    global save_folder
    save_folder = filedialog.askdirectory()
    path2.set(save_folder)
    
## ============================ Error check =============================
def Error(ARW_folder, save_folder, img_format):
    wrong_flag = 1
    if len(ARW_folder) < 5:
       messagebox.showerror("Error", "Please choose correct ARW image folder!")
    elif len(save_folder) < 5:
       messagebox.showerror("Error", "Please choose correct save image folder!")
    elif len(img_format) < 2:
       messagebox.showerror("Error", "Please choose correct image format!")
    else:
        wrong_flag = 0
    return wrong_flag

## ============================ function implement ===================================
class Convert(threading.Thread):
    def __init__(self, window, ARW_folder, save_folder, img_format):
      threading.Thread.__init__(self)
      self.window = window
      self.ARW_folder = ARW_folder
      self.save_folder = save_folder
      self.img_format = img_format
      if Error(ARW_folder, save_folder, img_format):
          return
      self.start()
      
    def run(self):
        Print_log(self.window, '轉換進行中，請稍後...', [190, 330])
        
        files = os.listdir(self.ARW_folder)
        os.chdir(self.ARW_folder)
        
        for f in files:
            raw = rawpy.imread(f)
            rgb = raw.postprocess()
            imageio.imsave(r'{}/{}.{}'.format(self.save_folder, f.split('.')[0], self.img_format), rgb)
            
        time.sleep(1) ## 睡一下，確保轉換有完成
        Print_log(self.window, '轉換完成!', [190, 350])
            
class Print_log(threading.Thread):
    def __init__(self, window, log, position):
      threading.Thread.__init__(self)
      self.window = window
      self.log = log
      self.position = position
      self.start()
      
    def run(self):
        log_printing = tk.Label(self.window, text=self.log)##產生lable
        log_printing.place(x=self.position[0], y=self.position[1], anchor=CENTER)
            


if __name__ == '__main__':
    ############### 基本構建 #################
    window = tk.Tk()
    window.title('ARW conversion')
    window.geometry('380x400')
    window.resizable(False, False)
    window.iconbitmap(r"C:\Users\User\Desktop\ARW_conversion\hachi.ico")
    ##########################################
    
    ## ========================== parameters default =============================
    ARW_folder = ""
    save_folder = ""
    img_format = ""
    
    ## ========================== close window button ===============================
    window_destroy_button = tk.Button(text="關閉", command=close_window) ##產生有選擇資料夾功能的button
    window_destroy_button.place(x=330,y=10)
    
    ## ============================ choose ARW folder =============================
    path1 = tk.StringVar()
    ARW_path_entry = tk.Entry(window, textvariable = path1, width= 40)
    ARW_path_entry.place(x=190,y=80, anchor=CENTER)

    ARW_path_button = tk.Button(text="ARW檔案照片資料夾", command=choose_ARW_folder) ##產生有選擇資料夾功能的button
    ARW_path_button.place(x=190,y=50,anchor=CENTER)
    
    ## ============================ choose save folder =============================
    path2 = tk.StringVar()
    save_path_entry = tk.Entry(window, textvariable = path2, width= 40)
    save_path_entry.place(x=190,y=160, anchor=CENTER)

    save_path_button = tk.Button(text="目的地資料夾", command=choose_save_folder) ##產生有選擇資料夾功能的button
    save_path_button.place(x=190,y=130,anchor=CENTER)
    
    ## ===========================  choose img format  ==============================
    ## log
    log_ongoing = tk.Label(window, text='轉換格式')##產生lable
    log_ongoing.place(x=190,y=220,anchor=CENTER)

    choose_img_format = ttk.Combobox(window, values=['jpg','png','jpeg'], width =  6)
    choose_img_format.place(x=190,y=240, anchor=CENTER)
    
    ## ===========================  convert button  ==============================
    convert_button = tk.Button(text="開始轉換!", command=lambda:Convert(window, ARW_folder, save_folder, choose_img_format.get()))
    convert_button.place(x=190,y=300,anchor=CENTER)
    
    window.mainloop()


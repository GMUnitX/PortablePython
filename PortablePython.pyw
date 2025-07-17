import os

with open("startfile.txt", "r", encoding="utf-8") as f:
    files = f.readlines()
    f.close()

for i in range(len(files)):
    try:
        if len(files[i]) >= 4 and files[i][-4:].lower() == ".pyw":
            os.popen("pythonw.exe "+files[i])
        else:
            os.popen("python.exe "+files[i])
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("错误", "{e}")

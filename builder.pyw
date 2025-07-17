import os
import shutil
import sys
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class PortablePythonBuilder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("便携Python构建器 - Made by GMUnitX.")
        self.geometry("500x200")
        self.resizable(False, False)
        self.python_paths = []
        self.selected_path = tk.StringVar()

        try:
            icon_path = os.path.join(os.path.dirname(__file__), "icon.ico")
            if os.path.isfile(icon_path):
                self.iconbitmap(icon_path)
        except:
            pass

        self.create_widgets()
        self.scan_python_paths()

    def create_widgets(self):
        # Python路径选择
        frame = ttk.LabelFrame(self, text="选择 Python 路径", padding=10)
        frame.pack(fill="x", padx=10, pady=5)

        # 一行放下拉框和按钮
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=5)

        self.path_combo = ttk.Combobox(row, textvariable=self.selected_path,
                                       width=40, state="readonly")
        self.path_combo.pack(side="left", fill="x", expand=True)

        browse_btn = ttk.Button(row, text="手动浏览", command=self.browse_path)
        browse_btn.pack(side="left", padx=(5, 0))

        # 进度条
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=5)

        # 状态标签
        self.status_label = ttk.Label(self, text="等待选择路径...")
        self.status_label.pack(pady=5)

        # 下一步按钮（右下角）
        self.next_btn = ttk.Button(self, text="下一步", command=self.start_process)
        self.next_btn.pack(anchor="se", padx=10, pady=10)

    def scan_python_paths(self):
        self.status_label.config(text="正在扫描 Python 安装路径...")
        self.update()

        paths = set()

        for path in os.environ.get("PATH", "").split(os.pathsep):
            py_path = os.path.join(path, "python.exe" if os.name == "nt" else "python")
            if os.path.isfile(py_path):
                paths.add(os.path.dirname(py_path))

        if os.name == "nt":
            try:
                result = subprocess.check_output(["py", "-0p"], text=True, stderr=subprocess.DEVNULL)
                for line in result.splitlines():
                    if "python.exe" in line:
                        parts = line.strip().split("\t")
                        if len(parts) >= 2:
                            path = parts[-1].strip()
                            if os.path.isfile(path):
                                paths.add(os.path.dirname(path))
            except Exception:
                pass

        self.python_paths = sorted(paths)
        self.path_combo["values"] = self.python_paths
        if self.python_paths:
            self.path_combo.current(0)
            self.selected_path.set(self.python_paths[0])

        self.status_label.config(text="扫描完成，请选择 Python 路径。")

    def browse_path(self):
        path = filedialog.askdirectory(title="选择 Python 安装目录")
        if path:
            if os.path.isfile(os.path.join(path, "python.exe" if os.name == "nt" else "python")):
                self.selected_path.set(path)
                self.path_combo.set(path)
            else:
                messagebox.showerror("无效路径", "该目录下未找到 Python 可执行文件。")

    def start_process(self):
        src_path = self.selected_path.get()
        if not src_path or not os.path.isdir(src_path):
            messagebox.showerror("路径无效", "请选择有效的 Python 安装路径。")
            return

        self.next_btn.config(state="disabled")
        self.progress["value"] = 0
        self.status_label.config(text="开始处理...")

        threading.Thread(target=self.build_portable_python, args=(src_path,), daemon=True).start()

    def build_portable_python(self, src_path):
        try:
            work_dir = os.getcwd()
            dest_path = os.path.join(work_dir, "PortablePython")
            resources_dir = os.path.join(work_dir, "Resources")

            self.update_status("正在删除旧目录...", 0)
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)

            self.update_status("正在复制 Python 目录...", 10)
            total_files = sum([len(files) for _, _, files in os.walk(src_path)])
            copied = 0

            def copy_with_progress(src, dst):
                nonlocal copied
                if os.path.isdir(src):
                    os.makedirs(dst, exist_ok=True)
                    for item in os.listdir(src):
                        s = os.path.join(src, item)
                        d = os.path.join(dst, item)
                        copy_with_progress(s, d)
                else:
                    shutil.copy2(src, dst)
                    copied += 1
                    progress = 10 + int((copied / total_files) * 70)
                    self.update_status("正在复制 Python 文件...", progress)

            copy_with_progress(src_path, dest_path)

            self.update_status("正在复制 Resources...", 85)
            if os.path.isdir(resources_dir):
                for item in os.listdir(resources_dir):
                    src = os.path.join(resources_dir, item)
                    dst = os.path.join(dest_path, item)
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    else:
                        shutil.copy2(src, dst)

            self.update_status("完成！", 100)
            messagebox.showinfo("完成", "PortablePython 创建成功，当前所在目录下的“PortablePython”文件夹即为便携Python。")
        except Exception as e:
            messagebox.showerror("错误", f"处理失败：\n{str(e)}")
        finally:
            self.next_btn.config(state="normal")

    def update_status(self, text, value):
        def _update():
            self.status_label.config(text=text)
            self.progress["value"] = value
        self.after(0, _update)

if __name__ == "__main__":
    app = PortablePythonBuilder()
    app.mainloop()

"""
Face Counter Launcher
=====================

Lightweight launcher hiển thị splash ngay lập tức,
sau đó tải về, giải nén và chạy main app.
"""

import tkinter as tk
import threading
import zipfile
import os
import sys
import subprocess
import math
import shutil
import urllib.request
import tempfile

# Cấu hình
APP_NAME = "FaceCounter"
APP_URL = "https://epllivescore.com/FaceCounterData.zip"
INSTALL_DIR = os.path.join(os.environ.get('LOCALAPPDATA', os.path.expanduser('~')), APP_NAME)
MAIN_EXE = os.path.join(INSTALL_DIR, "FaceCounter", "FaceCounter.exe")


class LauncherSplash:
    """Launcher với splash screen, download và progress bar"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        
        # Màu sắc
        self.bg_color = "#1a1a2e"
        self.accent_color = "#e94560"
        self.text_color = "#eaeaea"
        
        # Kích thước
        width, height = 500, 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.overrideredirect(True)
        self.root.configure(bg=self.bg_color)
        
        # Animation
        self.angle = 0
        self.running = True
        self.progress = 0
        self.status_text = "Đang khởi động..."
        self.sub_status = ""
        
        self._create_widgets()
        self._animate()
        
        # Bắt đầu kiểm tra và chạy app
        self.root.after(100, self._start_process)
        
    def _create_widgets(self):
        """Tạo UI"""
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(expand=True, fill=tk.BOTH, padx=20)
        
        # Logo
        tk.Label(
            container,
            text="🔍",
            font=("Segoe UI Emoji", 48),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(pady=(20, 10))
        
        # Title
        tk.Label(
            container,
            text="Face Counter",
            font=("Segoe UI", 24, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        ).pack()
        
        # Subtitle
        tk.Label(
            container,
            text="Tool Đếm Khuôn Mặt Trong Ảnh",
            font=("Segoe UI", 10),
            fg="#888",
            bg=self.bg_color
        ).pack(pady=(5, 15))
        
        # Spinner
        self.canvas = tk.Canvas(
            container,
            width=60,
            height=60,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Progress bar
        progress_frame = tk.Frame(container, bg=self.bg_color)
        progress_frame.pack(pady=10, fill=tk.X)
        
        self.progress_bg = tk.Canvas(
            progress_frame,
            width=350,
            height=10,
            bg="#333",
            highlightthickness=0
        )
        self.progress_bg.pack()
        
        # Status text chính
        self.status_label = tk.Label(
            container,
            text=self.status_text,
            font=("Segoe UI", 11, "bold"),
            fg="#ffd93d",
            bg=self.bg_color
        )
        self.status_label.pack(pady=(10, 2))
        
        # Sub status (cho chi tiết như tốc độ download)
        self.sub_status_label = tk.Label(
            container,
            text="",
            font=("Segoe UI", 9),
            fg="#888",
            bg=self.bg_color
        )
        self.sub_status_label.pack(pady=(0, 10))
        
        # Version
        tk.Label(
            container,
            text="v1.0",
            font=("Segoe UI", 8),
            fg="#555",
            bg=self.bg_color
        ).pack(pady=(10, 5))
        
    def _draw_spinner(self):
        """Vẽ spinner"""
        self.canvas.delete("all")
        cx, cy, radius, num_dots = 30, 30, 20, 8
        
        for i in range(num_dots):
            angle_rad = math.radians(self.angle + i * 45)
            x = cx + radius * math.cos(angle_rad)
            y = cy + radius * math.sin(angle_rad)
            size = 6 - (i * 0.5)
            opacity = 255 - (i * 25)
            color = f"#{opacity:02x}{69:02x}{96:02x}"
            
            if size > 0:
                self.canvas.create_oval(x-size, y-size, x+size, y+size, fill=color, outline="")
                
    def _draw_progress(self):
        """Vẽ progress bar"""
        self.progress_bg.delete("all")
        self.progress_bg.create_rectangle(0, 0, 350, 10, fill="#333", outline="")
        if self.progress > 0:
            width = int(350 * self.progress / 100)
            self.progress_bg.create_rectangle(0, 0, width, 10, fill=self.accent_color, outline="")
            
    def _animate(self):
        """Animation loop"""
        if not self.running:
            return
        self.angle -= 15
        self._draw_spinner()
        self._draw_progress()
        self.status_label.config(text=self.status_text)
        self.sub_status_label.config(text=self.sub_status)
        self.root.after(50, self._animate)
        
    def _update_status(self, text, progress=None, sub=""):
        """Cập nhật status"""
        self.status_text = text
        self.sub_status = sub
        if progress is not None:
            self.progress = progress
            
    def _format_size(self, bytes):
        """Format byte size"""
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024 * 1024:
            return f"{bytes/1024:.1f} KB"
        else:
            return f"{bytes/(1024*1024):.1f} MB"
            
    def _start_process(self):
        """Bắt đầu quá trình kiểm tra/tải/giải nén"""
        def process():
            try:
                # Kiểm tra app đã được cài đặt chưa
                if os.path.exists(MAIN_EXE):
                    self._update_status("Đang khởi động ứng dụng...", 100)
                    self.root.after(500, lambda: self._launch_app())
                    return
                
                # Tạo thư mục tạm để download
                temp_dir = tempfile.gettempdir()
                zip_path = os.path.join(temp_dir, "FaceCounterData.zip")
                
                # Download file
                self._update_status("Đang tải ứng dụng...", 5, "Đang kết nối...")
                
                try:
                    # Lấy thông tin file
                    req = urllib.request.Request(APP_URL, headers={'User-Agent': 'FaceCounter/1.0'})
                    response = urllib.request.urlopen(req, timeout=30)
                    total_size = int(response.headers.get('Content-Length', 0))
                    
                    # Download với progress
                    downloaded = 0
                    chunk_size = 1024 * 64  # 64KB chunks
                    
                    with open(zip_path, 'wb') as f:
                        while True:
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            
                            if total_size > 0:
                                progress = 5 + int(45 * downloaded / total_size)
                                percent = int(100 * downloaded / total_size)
                                self._update_status(
                                    f"Đang tải... {percent}%",
                                    progress,
                                    f"{self._format_size(downloaded)} / {self._format_size(total_size)}"
                                )
                            else:
                                self._update_status(
                                    "Đang tải...",
                                    30,
                                    f"Đã tải: {self._format_size(downloaded)}"
                                )
                                
                except Exception as e:
                    self._update_status(f"❌ Lỗi tải: {str(e)}", 0)
                    self.root.after(5000, self.root.destroy)
                    return
                
                # Tạo thư mục cài đặt
                os.makedirs(INSTALL_DIR, exist_ok=True)
                
                # Giải nén
                self._update_status("Đang giải nén...", 55, "Vui lòng đợi...")
                
                with zipfile.ZipFile(zip_path, 'r') as zf:
                    files = zf.namelist()
                    total = len(files)
                    
                    for i, file in enumerate(files):
                        zf.extract(file, INSTALL_DIR)
                        progress = 55 + int(40 * (i + 1) / total)
                        self._update_status(
                            f"Đang giải nén... {int((i+1)*100/total)}%",
                            progress,
                            f"{i+1}/{total} files"
                        )
                
                # Xóa file zip tạm
                try:
                    os.remove(zip_path)
                except:
                    pass
                        
                self._update_status("Đang khởi động ứng dụng...", 100, "")
                self.root.after(500, lambda: self._launch_app())
                
            except Exception as e:
                self._update_status(f"❌ Lỗi: {str(e)}", 0)
                self.root.after(5000, self.root.destroy)
                
        threading.Thread(target=process, daemon=True).start()
        
    def _launch_app(self):
        """Chạy main app"""
        self.running = False
        self.root.destroy()
        
        if os.path.exists(MAIN_EXE):
            subprocess.Popen([MAIN_EXE], cwd=os.path.dirname(MAIN_EXE))
        
    def run(self):
        """Chạy launcher"""
        self.root.mainloop()


def main():
    launcher = LauncherSplash()
    launcher.run()


if __name__ == "__main__":
    main()

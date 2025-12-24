"""
Tool Đếm Khuôn Mặt Trong Ảnh
============================

Ứng dụng GUI sử dụng YOLOv8 để phát hiện và đếm số khuôn mặt trong ảnh.
Mỗi khuôn mặt được đánh dấu bằng số thứ tự.

Cách sử dụng:
    python main.py

Yêu cầu:
    - Python 3.10+
    - Cài đặt dependencies: pip install -r requirements.txt
"""

import tkinter as tk
import threading
import sys
import os
import math

# Thêm thư mục hiện tại vào path (cho PyInstaller)
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))


class SplashAndApp:
    """Splash screen và App trong cùng một cửa sổ"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        
        # Màu sắc
        self.bg_color = "#1a1a2e"
        self.accent_color = "#e94560"
        self.text_color = "#eaeaea"
        
        # Kích thước splash
        self.splash_width = 400
        self.splash_height = 300
        
        # Căn giữa màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.splash_width) // 2
        y = (screen_height - self.splash_height) // 2
        
        self.root.geometry(f"{self.splash_width}x{self.splash_height}+{x}+{y}")
        self.root.overrideredirect(True)  # Ẩn title bar
        self.root.configure(bg=self.bg_color)
        
        # Animation variables
        self.angle = 0
        self.dots = 0
        self.loading = True
        
        # Tạo splash UI
        self._create_splash()
        
        # Bắt đầu load trong background
        self.root.after(100, self._start_loading)
        
        # Bắt đầu animation
        self._animate()
        
    def _create_splash(self):
        """Tạo splash screen UI"""
        self.splash_frame = tk.Frame(self.root, bg=self.bg_color)
        self.splash_frame.pack(expand=True, fill=tk.BOTH)
        
        container = tk.Frame(self.splash_frame, bg=self.bg_color)
        container.pack(expand=True)
        
        # Icon
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
        ).pack(pady=(5, 20))
        
        # Spinner canvas
        self.canvas = tk.Canvas(
            container,
            width=60,
            height=60,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(pady=10)
        
        # Loading text
        self.loading_label = tk.Label(
            container,
            text="Đang khởi động",
            font=("Segoe UI", 11),
            fg="#ffd93d",
            bg=self.bg_color
        )
        self.loading_label.pack(pady=10)
        
        # Version
        tk.Label(
            container,
            text="v1.0",
            font=("Segoe UI", 8),
            fg="#555",
            bg=self.bg_color
        ).pack(pady=(10, 5))
        
    def _draw_spinner(self):
        """Vẽ spinner animation"""
        self.canvas.delete("all")
        
        cx, cy = 30, 30
        radius = 20
        num_dots = 8
        
        for i in range(num_dots):
            angle_rad = math.radians(self.angle + i * (360 / num_dots))
            x = cx + radius * math.cos(angle_rad)
            y = cy + radius * math.sin(angle_rad)
            
            size = 6 - (i * 0.5)
            opacity = 255 - (i * 25)
            color = f"#{opacity:02x}{69:02x}{96:02x}"
            
            if size > 0:
                self.canvas.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill=color,
                    outline=""
                )
        
    def _animate(self):
        """Animation loop"""
        if not self.loading:
            return
            
        self.angle -= 15
        self._draw_spinner()
        
        dots_text = "." * (self.dots % 4)
        self.loading_label.config(text=f"Đang khởi động{dots_text}")
        self.dots += 1
        
        self.root.after(50, self._animate)
        
    def _start_loading(self):
        """Bắt đầu load app trong background"""
        def load():
            # Import các module nặng
            from app import PersonCounterApp
            from person_detector import PersonDetector
            
            # Báo hiệu load xong
            self.root.after(0, lambda: self._show_main_app(PersonCounterApp))
            
        threading.Thread(target=load, daemon=True).start()
        
    def _show_main_app(self, app_class):
        """Chuyển sang main app"""
        self.loading = False
        
        # Xóa splash
        self.splash_frame.destroy()
        
        # Cấu hình lại window cho app chính
        self.root.overrideredirect(False)
        self.root.title("🔍 Tool Đếm Khuôn Mặt Trong Ảnh")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Căn giữa màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 1000) // 2
        y = (screen_height - 700) // 2
        self.root.geometry(f"1000x700+{x}+{y}")
        
        # Tạo app
        app_class(self.root)
        
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


def main():
    """Entry point"""
    app = SplashAndApp()
    app.run()


if __name__ == "__main__":
    main()

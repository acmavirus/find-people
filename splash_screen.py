"""
Splash Screen Module
Hiển thị màn hình loading khi ứng dụng khởi động
"""

import tkinter as tk
import threading
import math


class SplashScreen:
    """Màn hình splash với loading animation"""
    
    def __init__(self):
        """Khởi tạo splash screen"""
        self.root = tk.Tk()
        self.root.title("")
        
        # Kích thước và vị trí
        width = 400
        height = 300
        
        # Căn giữa màn hình
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Ẩn title bar
        self.root.overrideredirect(True)
        
        # Màu sắc
        self.bg_color = "#1a1a2e"
        self.accent_color = "#e94560"
        self.text_color = "#eaeaea"
        
        self.root.configure(bg=self.bg_color)
        
        # Animation variables
        self.angle = 0
        self.dots = 0
        self.running = True
        
        # Tạo giao diện
        self._create_widgets()
        
        # Bắt đầu animation
        self._animate()
        
    def _create_widgets(self):
        """Tạo các widget"""
        # Container
        container = tk.Frame(self.root, bg=self.bg_color)
        container.pack(expand=True)
        
        # Icon/Logo
        self.logo_label = tk.Label(
            container,
            text="🔍",
            font=("Segoe UI Emoji", 48),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.logo_label.pack(pady=(20, 10))
        
        # Title
        title_label = tk.Label(
            container,
            text="Face Counter",
            font=("Segoe UI", 24, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            container,
            text="Tool Đếm Khuôn Mặt Trong Ảnh",
            font=("Segoe UI", 10),
            fg="#888",
            bg=self.bg_color
        )
        subtitle_label.pack(pady=(5, 20))
        
        # Canvas cho spinner animation
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
        version_label = tk.Label(
            container,
            text="v1.0",
            font=("Segoe UI", 8),
            fg="#555",
            bg=self.bg_color
        )
        version_label.pack(pady=(10, 5))
        
    def _draw_spinner(self):
        """Vẽ spinner animation"""
        self.canvas.delete("all")
        
        cx, cy = 30, 30  # Center
        radius = 20
        
        # Vẽ các chấm xung quanh
        num_dots = 8
        for i in range(num_dots):
            angle_rad = math.radians(self.angle + i * (360 / num_dots))
            x = cx + radius * math.cos(angle_rad)
            y = cy + radius * math.sin(angle_rad)
            
            # Độ lớn và màu sắc giảm dần
            size = 6 - (i * 0.5)
            opacity = 255 - (i * 25)
            
            # Tạo màu với opacity khác nhau
            color = f"#{opacity:02x}{69:02x}{96:02x}"  # Gradient của accent color
            
            if size > 0:
                self.canvas.create_oval(
                    x - size, y - size,
                    x + size, y + size,
                    fill=color,
                    outline=""
                )
        
    def _animate(self):
        """Animation loop"""
        if not self.running:
            return
            
        # Update spinner
        self.angle -= 15  # Xoay ngược chiều kim đồng hồ
        self._draw_spinner()
        
        # Update loading text với dots
        dots_text = "." * (self.dots % 4)
        self.loading_label.config(text=f"Đang khởi động{dots_text}")
        self.dots += 1
        
        # Tiếp tục animation
        self.root.after(50, self._animate)
        
    def close(self):
        """Đóng splash screen"""
        self.running = False
        self.root.destroy()
        
    def run_with_callback(self, callback):
        """
        Chạy splash screen và gọi callback sau khi hiển thị
        
        Args:
            callback: Hàm sẽ được gọi để load app chính
        """
        def load_in_background():
            result = callback()
            # Đóng splash sau khi load xong
            self.root.after(0, lambda: self._finish_loading(result))
            
        # Bắt đầu load sau 100ms để splash hiển thị trước
        self.root.after(100, lambda: threading.Thread(
            target=load_in_background,
            daemon=True
        ).start())
        
        # Chạy mainloop
        self.root.mainloop()
        
    def _finish_loading(self, app_root):
        """Hoàn tất loading và hiển thị app chính"""
        self.close()
        if app_root:
            app_root.mainloop()


def show_splash_and_load(app_class):
    """
    Hiển thị splash screen và load app
    
    Args:
        app_class: Class của ứng dụng chính
    """
    splash = SplashScreen()
    
    main_root = None
    main_app = None
    
    def load_app():
        nonlocal main_root, main_app
        # Import nặng ở đây
        from person_detector import PersonDetector
        
        # Tạo root window (ẩn)
        main_root = tk.Tk()
        main_root.withdraw()  # Ẩn trước
        
        # Tạo app
        main_app = app_class(main_root)
        
        return main_root
        
    def finish():
        splash.close()
        if main_root:
            main_root.deiconify()  # Hiện window
            main_root.mainloop()
    
    # Load trong background
    def background_load():
        load_app()
        splash.root.after(500, finish)  # Delay thêm 500ms cho đẹp
        
    splash.root.after(100, lambda: threading.Thread(
        target=background_load,
        daemon=True
    ).start())
    
    splash.root.mainloop()


if __name__ == "__main__":
    # Test splash screen
    splash = SplashScreen()
    splash.root.after(3000, splash.close)  # Tự đóng sau 3s
    splash.root.mainloop()

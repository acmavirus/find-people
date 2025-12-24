"""
Person Counter App - GUI Application
Ứng dụng đếm số người trong ảnh với giao diện Tkinter
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import threading

from person_detector import PersonDetector


class PersonCounterApp:
    """Ứng dụng GUI đếm người trong ảnh"""
    
    def __init__(self, root: tk.Tk):
        """Khởi tạo ứng dụng"""
        self.root = root
        self.root.title("🔍 Tool Đếm Khuôn Mặt Trong Ảnh")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Màu sắc theme
        self.bg_color = "#1a1a2e"
        self.secondary_bg = "#16213e"
        self.accent_color = "#e94560"
        self.text_color = "#eaeaea"
        
        self.root.configure(bg=self.bg_color)
        
        # Biến lưu trữ
        self.current_image_path = None
        self.result_image = None
        self.detector = None
        self.photo_image = None  # Giữ reference để tránh garbage collection
        
        # Tạo giao diện
        self._create_widgets()
        
        # Load model trong background
        self._load_model_async()
        
    def _create_widgets(self):
        """Tạo các widget cho giao diện"""
        
        # === Header Frame ===
        header_frame = tk.Frame(self.root, bg=self.secondary_bg, pady=15)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="🔍 TOOL ĐẾM KHUÔN MẶT TRONG ẢNH",
            font=("Segoe UI", 20, "bold"),
            fg=self.text_color,
            bg=self.secondary_bg
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Sử dụng AI để phát hiện và đếm khuôn mặt",
            font=("Segoe UI", 10),
            fg="#888",
            bg=self.secondary_bg
        )
        subtitle_label.pack()
        
        # === Control Frame ===
        control_frame = tk.Frame(self.root, bg=self.bg_color, pady=10)
        control_frame.pack(fill=tk.X, padx=20)
        
        # Button chọn ảnh
        self.select_btn = tk.Button(
            control_frame,
            text="📁 Chọn Ảnh",
            font=("Segoe UI", 12, "bold"),
            bg=self.accent_color,
            fg="white",
            activebackground="#c73e54",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
            command=self._select_image
        )
        self.select_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            control_frame,
            text="⏳ Đang tải model AI...",
            font=("Segoe UI", 10),
            fg="#ffd93d",
            bg=self.bg_color
        )
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # Kết quả đếm
        self.count_label = tk.Label(
            control_frame,
            text="",
            font=("Segoe UI", 14, "bold"),
            fg="#4ecca3",
            bg=self.bg_color
        )
        self.count_label.pack(side=tk.RIGHT, padx=10)
        
        # === Image Display Frame ===
        image_frame = tk.Frame(self.root, bg=self.secondary_bg)
        image_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Canvas để hiển thị ảnh
        self.canvas = tk.Canvas(
            image_frame,
            bg=self.secondary_bg,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Placeholder text
        self.placeholder_id = self.canvas.create_text(
            0, 0,
            text="📷 Chọn ảnh để bắt đầu phát hiện khuôn mặt",
            font=("Segoe UI", 14),
            fill="#666"
        )
        
        # Bind resize event
        self.canvas.bind("<Configure>", self._on_canvas_resize)
        
        # === Footer Frame ===
        footer_frame = tk.Frame(self.root, bg=self.secondary_bg, pady=8)
        footer_frame.pack(fill=tk.X)
        
        footer_label = tk.Label(
            footer_frame,
            text="💡 Mỗi khuôn mặt được đánh dấu bằng số thứ tự và khung màu",
            font=("Segoe UI", 9),
            fg="#888",
            bg=self.secondary_bg
        )
        footer_label.pack()
        
    def _on_canvas_resize(self, event):
        """Xử lý khi canvas thay đổi kích thước"""
        # Cập nhật vị trí placeholder
        self.canvas.coords(
            self.placeholder_id,
            event.width // 2,
            event.height // 2
        )
        
        # Nếu có ảnh, vẽ lại
        if self.result_image:
            self._display_image(self.result_image)
            
    def _load_model_async(self):
        """Load model trong background thread"""
        def load():
            try:
                self.detector = PersonDetector()
                self.root.after(0, lambda: self.status_label.config(
                    text="✅ Sẵn sàng!",
                    fg="#4ecca3"
                ))
                self.root.after(0, lambda: self.select_btn.config(state=tk.NORMAL))
            except Exception as e:
                self.root.after(0, lambda: self.status_label.config(
                    text=f"❌ Lỗi: {str(e)}",
                    fg="#ff6b6b"
                ))
                
        self.select_btn.config(state=tk.DISABLED)
        thread = threading.Thread(target=load, daemon=True)
        thread.start()
        
    def _select_image(self):
        """Mở dialog chọn ảnh"""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.webp"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("PNG files", "*.png"),
            ("All files", "*.*")
        ]
        
        filepath = filedialog.askopenfilename(
            title="Chọn ảnh để phát hiện khuôn mặt",
            filetypes=filetypes
        )
        
        if filepath:
            self.current_image_path = filepath
            self._process_image(filepath)
            
    def _process_image(self, image_path: str):
        """Xử lý ảnh và hiển thị kết quả"""
        
        # Hiển thị trạng thái đang xử lý
        self.status_label.config(text="⏳ Đang phát hiện khuôn mặt...", fg="#ffd93d")
        self.count_label.config(text="")
        self.select_btn.config(state=tk.DISABLED)
        self.root.update()
        
        def process():
            try:
                # Phát hiện người
                detections = self.detector.detect(image_path)
                
                # Vẽ kết quả
                result_image = self.detector.draw_results(image_path, detections)
                
                # Cập nhật UI trong main thread
                def update_ui():
                    self.result_image = result_image
                    self._display_image(result_image)
                    
                    person_count = len(detections)
                    if person_count == 0:
                        self.count_label.config(
                            text="Không tìm thấy khuôn mặt nào",
                            fg="#ff6b6b"
                        )
                    else:
                        self.count_label.config(
                            text=f"👤 Tìm thấy {person_count} khuôn mặt",
                            fg="#4ecca3"
                        )
                    
                    self.status_label.config(text="✅ Hoàn tất!", fg="#4ecca3")
                    self.select_btn.config(state=tk.NORMAL)
                    
                self.root.after(0, update_ui)
                
            except Exception as e:
                def show_error():
                    self.status_label.config(
                        text=f"❌ Lỗi: {str(e)}",
                        fg="#ff6b6b"
                    )
                    self.select_btn.config(state=tk.NORMAL)
                    messagebox.showerror("Lỗi", f"Không thể xử lý ảnh:\n{str(e)}")
                    
                self.root.after(0, show_error)
                
        thread = threading.Thread(target=process, daemon=True)
        thread.start()
        
    def _display_image(self, image: Image.Image):
        """Hiển thị ảnh trên canvas với resize phù hợp"""
        
        # Ẩn placeholder
        self.canvas.itemconfig(self.placeholder_id, state='hidden')
        
        # Lấy kích thước canvas
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width < 10 or canvas_height < 10:
            return
            
        # Tính toán kích thước mới giữ tỉ lệ
        img_width, img_height = image.size
        
        ratio = min(
            (canvas_width - 20) / img_width,
            (canvas_height - 20) / img_height
        )
        
        new_width = int(img_width * ratio)
        new_height = int(img_height * ratio)
        
        # Resize ảnh
        resized = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Convert sang PhotoImage
        self.photo_image = ImageTk.PhotoImage(resized)
        
        # Xóa ảnh cũ và vẽ ảnh mới
        self.canvas.delete("image")
        self.canvas.create_image(
            canvas_width // 2,
            canvas_height // 2,
            image=self.photo_image,
            anchor=tk.CENTER,
            tags="image"
        )


def main():
    """Entry point"""
    root = tk.Tk()
    app = PersonCounterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

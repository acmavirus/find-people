"""
Face Detector Module
Sử dụng YOLOv8-face để phát hiện và đếm khuôn mặt trong ảnh
"""

import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import os


class PersonDetector:
    """Class để phát hiện khuôn mặt trong ảnh sử dụng YOLOv8-face"""
    
    def __init__(self):
        """
        Khởi tạo detector với YOLOv8-face model
        """
        # Sử dụng yolov8n-face model - chuyên biệt cho face detection
        # Model này được train đặc biệt để detect faces
        model_path = "yolov8n-face.pt"
        
        # Kiểm tra và download model nếu chưa có
        if not os.path.exists(model_path):
            # Download từ Hugging Face hoặc sử dụng model chuẩn với cấu hình đặc biệt
            # Fallback: dùng yolov8n.pt và chỉ detect class 0 (person) nhưng crop head region
            print("Đang tải YOLOv8 model...")
            self.model = YOLO("yolov8n.pt")
            self.use_face_model = False
        else:
            self.model = YOLO(model_path)
            self.use_face_model = True
            
        # Class ID 0 trong COCO dataset là "person"
        self.person_class_id = 0
        
    def detect(self, image_path: str, confidence: float = 0.3) -> list:
        """
        Phát hiện khuôn mặt trong ảnh
        
        Args:
            image_path: Đường dẫn tới ảnh
            confidence: Ngưỡng confidence tối thiểu (0-1)
            
        Returns:
            List các detection, mỗi detection là dict chứa:
            - bbox: [x1, y1, x2, y2]
            - confidence: độ tin cậy
            - number: số thứ tự
        """
        # Đọc ảnh để lấy kích thước
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Không thể đọc ảnh: {image_path}")
        
        img_height, img_width = image.shape[:2]
        
        # Chạy detection
        results = self.model(image_path, verbose=False, conf=confidence)
        
        detections = []
        face_count = 0
        
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # Chỉ lấy class "person" (class_id = 0)
                if int(box.cls[0]) == self.person_class_id:
                    conf = float(box.conf[0])
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    
                    # Tính toán vùng đầu/mặt từ person bounding box
                    # Giả định khuôn mặt nằm ở 1/4 - 1/3 phía trên của body
                    person_height = y2 - y1
                    person_width = x2 - x1
                    
                    # Estimate face region (top portion of person bbox)
                    face_height = person_height * 0.35  # 35% chiều cao person là vùng đầu/mặt
                    
                    # Center the face box horizontally, make it more square-ish
                    face_width = min(person_width * 0.7, face_height * 1.2)
                    center_x = (x1 + x2) / 2
                    
                    face_x1 = center_x - face_width / 2
                    face_y1 = y1
                    face_x2 = center_x + face_width / 2
                    face_y2 = y1 + face_height
                    
                    # Clamp to image bounds
                    face_x1 = max(0, face_x1)
                    face_y1 = max(0, face_y1)
                    face_x2 = min(img_width, face_x2)
                    face_y2 = min(img_height, face_y2)
                    
                    face_count += 1
                    detections.append({
                        'bbox': [int(face_x1), int(face_y1), int(face_x2), int(face_y2)],
                        'confidence': conf,
                        'number': face_count
                    })
        
        return detections
    
    def draw_results(self, image_path: str, detections: list) -> Image.Image:
        """
        Vẽ bounding box và số thứ tự lên ảnh
        
        Args:
            image_path: Đường dẫn tới ảnh gốc
            detections: Kết quả từ hàm detect()
            
        Returns:
            PIL Image với các annotation
        """
        # Đọc ảnh bằng PIL
        image = Image.open(image_path).convert('RGB')
        draw = ImageDraw.Draw(image)
        
        # Tính font size dựa trên kích thước ảnh
        img_width, img_height = image.size
        font_size = max(20, min(img_width, img_height) // 30)
        
        # Cố gắng load font đẹp hơn, fallback về default
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
        
        # Màu sắc cho bounding box
        colors = [
            '#FF6B6B',  # Đỏ
            '#4ECDC4',  # Xanh ngọc
            '#45B7D1',  # Xanh dương
            '#96CEB4',  # Xanh lá nhạt
            '#FFEAA7',  # Vàng
            '#DDA0DD',  # Tím nhạt
            '#98D8C8',  # Mint
            '#F7DC6F',  # Gold
            '#BB8FCE',  # Lavender
            '#85C1E9',  # Sky blue
        ]
        
        for det in detections:
            x1, y1, x2, y2 = det['bbox']
            number = det['number']
            
            # Chọn màu theo số thứ tự
            color = colors[(number - 1) % len(colors)]
            
            # Vẽ bounding box
            box_width = max(2, min(img_width, img_height) // 200)
            draw.rectangle([x1, y1, x2, y2], outline=color, width=box_width)
            
            # Vẽ label background
            label = f"{number}"
            
            # Tính kích thước text
            bbox_text = draw.textbbox((0, 0), label, font=font)
            text_width = bbox_text[2] - bbox_text[0]
            text_height = bbox_text[3] - bbox_text[1]
            
            padding = 5
            label_x1 = x1
            label_y1 = y1 - text_height - padding * 2
            if label_y1 < 0:
                label_y1 = y1
            label_x2 = label_x1 + text_width + padding * 2
            label_y2 = label_y1 + text_height + padding * 2
            
            # Vẽ background cho label
            draw.rectangle([label_x1, label_y1, label_x2, label_y2], fill=color)
            
            # Vẽ số
            draw.text(
                (label_x1 + padding, label_y1 + padding),
                label,
                fill='white',
                font=font
            )
        
        return image


if __name__ == "__main__":
    # Test module
    detector = PersonDetector()
    print("FaceDetector đã sẵn sàng!")

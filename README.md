# 🔍 Tool Đếm Khuôn Mặt Trong Ảnh

Ứng dụng GUI sử dụng AI (YOLOv8) để phát hiện và đếm số khuôn mặt trong ảnh.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green.svg)

## 🔄 Sơ đồ hoạt động

```mermaid
flowchart TD
    A["🖱️ Double-click FaceCounter.exe"] --> B["� Giải nén files<br/>(~5-10 giây)"]
    B --> C["�🔄 Splash Screen<br/>Loading Animation"]
    C --> D{"⏳ Tải AI Model<br/>YOLOv8"}
    D --> E["🖼️ Main App<br/>Giao diện chính"]
    E --> F["📁 Chọn Ảnh"]
    F --> G["🤖 AI Phát hiện<br/>Khuôn mặt"]
    G --> H["🔢 Đánh số<br/>từng khuôn mặt"]
    H --> I["✅ Hiển thị kết quả"]
    I --> F
    
    style A fill:#e94560,color:#fff
    style B fill:#ff9f43,color:#000
    style C fill:#ffd93d,color:#000
    style D fill:#4ecdc4,color:#000
    style E fill:#1a1a2e,color:#fff
    style I fill:#4ecca3,color:#000
```

> ⚠️ **Lưu ý**: Bước "Giải nén files" là do PyInstaller `--onefile` mode cần giải nén ~343MB vào thư mục tạm trước khi chạy. Lần chạy sau sẽ nhanh hơn nếu files đã được cache.

## ✨ Tính năng

- 📷 Hỗ trợ: JPG, PNG, BMP, GIF, WebP
- 🤖 AI YOLOv8 phát hiện khuôn mặt
- 🔢 Đánh số thứ tự cho mỗi khuôn mặt
- 🎨 Giao diện Dark theme đẹp mắt
- 🔄 Splash screen loading animation
- ⚡ Hỗ trợ CPU và GPU

## 🚀 Sử dụng

### Cách 1: Chạy file EXE (Khuyên dùng)
```
Double-click file: dist/FaceCounter.exe
```

### Cách 2: Chạy từ Python
```bash
pip install -r requirements.txt
python main.py
```

## 📖 Hướng dẫn

1. Double-click `FaceCounter.exe`
2. Đợi splash screen loading
3. Click **"Chọn Ảnh"**
4. Xem kết quả với số thứ tự trên mỗi khuôn mặt

## 🛠️ Cấu trúc

```
tool-find-human/
├── main.py              # Entry point + Splash screen
├── app.py               # GUI Tkinter
├── person_detector.py   # Face detection
├── splash_screen.py     # Splash screen module
├── requirements.txt     # Dependencies
├── dist/
│   └── FaceCounter.exe  # Standalone EXE
└── README.md
```

## 📝 Ghi chú

- Lần đầu chạy sẽ download model YOLOv8 (~6MB)
- EXE có dung lượng ~343MB (bao gồm Python + AI)

## 📄 License

MIT License


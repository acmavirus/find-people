# 🔍 Tool Đếm Người Trong Ảnh

Ứng dụng GUI sử dụng AI (YOLOv8) để phát hiện và đếm số người xuất hiện trong ảnh.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green.svg)

## ✨ Tính năng

- 📷 Hỗ trợ nhiều định dạng ảnh: JPG, PNG, BMP, GIF, WebP
- 🤖 Sử dụng YOLOv8 - model AI tiên tiến để phát hiện người
- 🔢 Đánh số thứ tự cho mỗi người được phát hiện
- 🎨 Giao diện GUI đẹp mắt, dễ sử dụng
- ⚡ Xử lý nhanh, hỗ trợ cả CPU và GPU

## 📋 Yêu cầu

- Python 3.10 trở lên
- Windows / macOS / Linux

## 🚀 Cài đặt

1. **Clone hoặc download project**

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng:**
```bash
python main.py
```

## 📖 Hướng dẫn sử dụng

1. Chạy ứng dụng bằng lệnh `python main.py`
2. Đợi model AI load xong (hiển thị "Sẵn sàng!")
3. Click nút **"Chọn Ảnh"** để chọn ảnh cần phân tích
4. Kết quả sẽ hiển thị:
   - Mỗi người được bao quanh bởi khung màu
   - Số thứ tự (1, 2, 3...) trên mỗi người
   - Tổng số người ở góc phải

## 🛠️ Cấu trúc Project

```
tool-find-human/
├── main.py              # Entry point
├── app.py               # GUI Tkinter
├── person_detector.py   # YOLOv8 detection
├── requirements.txt     # Dependencies
└── README.md            # Hướng dẫn
```

## 📝 Ghi chú

- Lần đầu chạy sẽ tự động download model YOLOv8 (~6MB)
- Cần kết nối internet cho lần đầu chạy
- Nếu có GPU NVIDIA + CUDA, ứng dụng sẽ tự động sử dụng GPU

## 📄 License

MIT License

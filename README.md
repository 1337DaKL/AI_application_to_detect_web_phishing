# 🛡️ AI Application to Detect Web Phishing

Ứng dụng AI sử dụng mô hình **XGBoost** để phát hiện và phân loại các trang web lừa đảo (phishing). Dự án bao gồm một **Chrome extension**, một **API server**, và một **mô hình học máy đã huấn luyện**.

---

# 📁 Cấu trúc dự án

.
├── XGBoost/ # Mã nguồn xử lý ML và mô hình
│ ├── app.py # Giao tiếp với mô hình
│ ├── extract_features.py# Trích xuất đặc trưng từ URL
│ ├── test_api.py # Kiểm thử API
│ └── xgboost_model.pkl # Mô hình đã huấn luyện
│
├── extension/ # Chrome Extension
│ ├── styles/ # File CSS
│ ├── background.html/js # Script chạy nền
│ ├── content.js # Script nhúng vào trang web
│ ├── popup.html # UI popup
│ └── manifest.json # Cấu hình extension
│
├── server/ # Server Flask chạy API
│ ├── templates/
│ │ └── view.html # Giao diện web nếu cần
│ └── app.py # Flask API endpoint
│
├── debug_output.html # Kết quả debug
└── README.md # Hướng dẫn (file này)


---

## 🔍 Chức năng chính

- Phân tích URL và trích xuất đặc trưng
- Dự đoán khả năng phishing bằng mô hình XGBoost
- Cung cấp API Flask để truy cập mô hình từ trình duyệt
- Chrome Extension giúp quét và cảnh báo người dùng

---

## 🛠️ Cài đặt

### 1. Cài đặt môi trường Python

```bash
pip install -r requirements.txt
Nếu chưa có requirements.txt, bạn có thể tạo:

pip freeze > requirements.txt
2. Chạy server Flask
cd server
python app.py
3. Gửi dữ liệu tới API (test nhanh)
curl -X POST http://127.0.0.1:5000/predict \
-H "Content-Type: application/json" \
-d "{\"url\": \"http://example.com\"}"
🧠 Huấn luyện mô hình (nếu cần)
cd XGBoost
python app.py  # hoặc script huấn luyện riêng nếu có
🌐 Cài đặt Extension
Mở trình duyệt Chrome và vào: chrome://extensions/

Bật Developer mode

Chọn “Load unpacked”

Trỏ tới thư mục extension/

Extension sẽ:

Lấy URL hiện tại

Gửi tới server Flask

Hiển thị kết quả trong popup

🧪 Test mô hình
cd XGBoost
python test_api.py

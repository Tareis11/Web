# Hệ thống tủ khóa thông minh

Hệ thống quản lý tủ khóa đơn giản với Python backend và HTML frontend.

## Tính năng chính

- Xem trạng thái các tủ (đang mở/đóng)
- Mở/khóa tủ
- Đặt mã cho tủ
- Xem lịch sử hoạt động

## Cài đặt

1. Cài đặt Python 3.8 trở lên
2. Cài đặt MongoDB
3. Tạo môi trường ảo và cài đặt thư viện:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Chạy ứng dụng

1. Khởi động MongoDB
2. Chạy backend:
```bash
cd backend
python app.py
```
3. Mở file `frontend/index.html` trong trình duyệt

## Cấu trúc thư mục

```
.
├── backend/
│   └── app.py          # Backend Flask
├── frontend/
│   ├── index.html      # Trang chủ
│   └── history.html    # Trang lịch sử
└── requirements.txt    # Thư viện Python
```

## API Endpoints

- `GET /api/lockers`: Lấy danh sách tủ
- `POST /api/lockers/toggle`: Mở/khóa tủ
- `POST /api/lockers/set-code`: Đặt mã cho tủ
- `GET /api/lockers/history`: Lấy lịch sử hoạt động

## Đóng góp

Mọi đóng góp đều được hoan nghênh! Vui lòng tạo issue hoặc pull request để đóng góp.

## Giấy phép

MIT License

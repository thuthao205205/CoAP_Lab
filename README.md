# THỰC HÀNH BUỔI 3 – LẬP TRÌNH PYTHON VỚI GIAO THỨC CoAP

## 1. Thông tin nhóm thực hiện

- **Môn học:** IoT và ứng dụng
- **Bài thực hành:** Buổi 3 – Lập trình Python với giao thức CoAP
- **Nhóm:** 20

### Danh sách thành viên

| STT | Họ và tên       | Mã sinh viên |
| :-: | --------------- | ------------ |
|  1  | Nguyễn Thu Thảo | B23DCCN776   |
|  2  | Lê Huy Hải      | B23DCCN272   |
|  3  | Phạm Thu Hà     | B23DCCN267   |

## 2. Môi trường thực hiện

- Hệ điều hành: Windows
- Ngôn ngữ: Python 3.12.10
- Thư viện: aiocoap 0.4.17
- Giao thức: CoAP qua UDP
- Cổng mặc định: 5683
- Địa chỉ Server: 127.0.0.1 (localhost)

### Cài đặt thư viện

```powershell
python --version
python -m pip install aiocoap
python -m pip show aiocoap
```

## 3. Cấu trúc dự án

```text
CoAP_Lab/
├── bai1/
│   ├── coap_server_bai1.py
│   └── coap_client_bai1.py
├── bai2/
│   ├── sensor_server_bai2.py
│   └── monitor_client_bai2.py
├── bai3/
│   ├── light_server_bai3.py
│   ├── light_controller_bai3.py
│   └── light_monitor_bai3.py
├── screenshots/
└── README.md
```

## 4. Bài 1 – CoAP GET và POST

**Mục tiêu:** Xây dựng CoAP Client–Server để gửi và nhận thông điệp.

**URI:** `coap://127.0.0.1:5683/iot/lab/message`

Chạy Server:

```powershell
python bai1\coap_server_bai1.py
```

Mở Terminal khác, chạy Client:

```powershell
python bai1\coap_client_bai1.py
```

**Kết quả đạt được:**

- Server xử lý yêu cầu GET và trả về lời chào.
- Client gửi POST chứa họ tên và mã sinh viên.
- Server hiển thị nội dung POST và thời gian nhận.
- Client nhận phản hồi `2.05 Content` và `2.04 Changed`.

## 5. Bài 2 – Mô phỏng cảm biến nhiệt độ và độ ẩm

**Mục tiêu:** Mô phỏng cảm biến và giám sát dữ liệu định kỳ.

**URI:** `coap://127.0.0.1:5683/iot/lab/sensor01/data`

Chạy Server:

```powershell
python bai2\sensor_server_bai2.py
```

Mở Terminal khác, chạy Client:

```powershell
python bai2\monitor_client_bai2.py
```

**Kết quả đạt được:**

- Server tạo dữ liệu nhiệt độ và độ ẩm ngẫu nhiên mỗi 3 giây.
- Client gửi GET định kỳ mỗi 3 giây.
- Server trả về JSON chứa `device_id`, `temperature`, `humidity`.
- Client cảnh báo khi nhiệt độ lớn hơn 35°C hoặc độ ẩm nhỏ hơn 40%.
- Client xử lý được trường hợp Server không phản hồi.

## 6. Bài 3 – Điều khiển đèn thông minh bằng CoAP Observe

**Mục tiêu:** Điều khiển và theo dõi trạng thái đèn thông minh.

**URI:** `coap://127.0.0.1:5683/iot/lab/light01/status`

Chạy Server:

```powershell
python bai3\light_server_bai3.py
```

Mở Terminal thứ hai, chạy Monitor:

```powershell
python bai3\light_monitor_bai3.py
```

Mở Terminal thứ ba, chạy Controller:

```powershell
python bai3\light_controller_bai3.py
```

**Các lệnh Controller:**

- `ON`: bật đèn.
- `OFF`: tắt đèn.
- `STATUS`: xem trạng thái.
- `EXIT`: thoát chương trình.

**Kết quả đạt được:**

- Server khởi tạo đèn ở trạng thái OFF.
- Controller điều khiển đèn bằng PUT và truy vấn bằng GET.
- Monitor đăng ký CoAP Observe thành công.
- Monitor tự động nhận thông báo khi trạng thái đèn thay đổi từ OFF sang ON hoặc ngược lại.
- Server chỉ phát thông báo khi trạng thái thực sự thay đổi.

## 7. Minh chứng kết quả

Ảnh chụp hoặc log chương trình được lưu trong thư mục `screenshots/`, bao gồm kết quả của Server và Client ở cả ba bài.

## 8. Lưu ý khi chạy

- Chạy Server trước Client.
- Bài 1, Bài 2 và Bài 3 cùng sử dụng cổng UDP 5683, vì vậy cần dừng Server của bài trước khi chuyển sang bài khác.
- Dùng `Ctrl+C` để dừng Server hoặc Monitoring Client.
- CoAP hoạt động trực tiếp qua UDP, không cần MQTT Broker.

## 9. Kết luận

Đã hoàn thành ba bài thực hành, qua đó tìm hiểu và triển khai các phương thức CoAP GET, POST, PUT, cơ chế truy vấn định kỳ và CoAP Observe trong mô phỏng hệ thống IoT bằng Python.

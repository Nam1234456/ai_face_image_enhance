**Khôi phục ảnh cũ bằng Deep Learning**

Repository này cung cấp mã nguồn, mô hình đã huấn luyện sẵn và công cụ demo cho bài toán **khôi phục ảnh cũ** (old photo restoration), bao gồm xử lý trầy xước, nhiễu, suy giảm chất lượng và tăng cường khuôn mặt.

---

## 🎯 Mục tiêu

- Khôi phục ảnh cũ, ảnh hỏng, ảnh lịch sử bằng mô hình học sâu
- Tự động:
  - Phát hiện và loại bỏ vết trầy xước
  - Giảm nhiễu, cải thiện độ sắc nét
  - Tăng cường chất lượng khuôn mặt trong ảnh chân dung
- Cung cấp pipeline hoàn chỉnh từ ảnh đầu vào → ảnh đã phục hồi

---

## ✨ Tính năng chính

- Pipeline khôi phục ảnh cũ end-to-end
- Mô hình xử lý **trầy xước (scratch)**
- Module **Face Enhancement** để cải thiện chi tiết khuôn mặt
- Hỗ trợ chạy bằng GPU (khuyến nghị) và CPU
- Có giao diện đồ họa (GUI) đơn giản để demo nhanh

---

## 🧱 Cấu trúc thư mục chính

```bash
Bringing-Old-Photos-Back-to-Life/
│
├── Global/ # Phục hồi tổng thể + phát hiện vết xước
├── Face_Enhancement/ # Tăng cường khuôn mặt
├── checkpoints/ # Mô hình đã huấn luyện
├── main.py # Giao diện chạy app
└── requirements.txt # File môi trường 
```

## ⚙️ Cài đặt

### 1. Clone repository

```bash
git clone 
cd 
```

### 2. Cài đặt các thư viện Python

```bash
pip install -r requirements.txt
```

```bash
cd Face_Enhancement/models/networks/
git clone https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
cp -rf Synchronized-BatchNorm-PyTorch/sync_batchnorm .
cd ../../../
```

```bash
cd Global/detection_models
git clone https://github.com/vacancy/Synchronized-BatchNorm-PyTorch
cp -rf Synchronized-BatchNorm-PyTorch/sync_batchnorm .
cd ../../
```

```bash
cd Face_Detection/
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bzip2 -d shape_predictor_68_face_landmarks.dat.bz2
cd ../
```

```bash
cd Face_Enhancement/
wget https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life/releases/download/v1.0/face_checkpoints.zip
unzip face_checkpoints.zip
cd ../
cd Global/
wget https://github.com/microsoft/Bringing-Old-Photos-Back-to-Life/releases/download/v1.0/global_checkpoints.zip
unzip global_checkpoints.zip
cd ../
```


## 🚀 Hướng dẫn sử dụng

### 🔁 Chạy ứng dụng
```bash
streamlit run main.py
```

Các bước:

1. Chọn ảnh đầu vào

2. Nhấn phục hồi ảnh

3. Xem kết quả output của từng stage

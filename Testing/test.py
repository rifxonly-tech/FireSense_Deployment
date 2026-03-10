import cv2
from ultralytics import YOLO

# 1. Muat model hasil training
# Pastikan nama file sesuai dengan yang kamu unduh
model = YOLO('best.pt') 

# 2. Buka koneksi ke webcam (0 biasanya untuk webcam bawaan laptop)
cap = cv2.VideoCapture(0)

print("Sistem FireSense Aktif! Arahkan api/asap ke kamera.")
print("Tekan tombol 'q' pada keyboard untuk mematikan sistem.")

while cap.isOpened():
    # Baca setiap frame dari kamera
    success, frame = cap.read()
    if not success:
        print("Kamera tidak terdeteksi.")
        break

    # 3. Jalankan deteksi YOLO
    # conf=0.5 artinya kita abaikan tebakan ragu-ragu di bawah 50%
    results = model(frame, conf=0.5)

    # 4. Gambar bounding box dan label ke atas gambar
    annotated_frame = results[0].plot()

    # 5. Tampilkan jendela live video
    cv2.imshow("FireSense - Live Detection Test", annotated_frame)

    # 6. Logika untuk keluar dari loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Bersihkan resource saat program ditutup
cap.release()
cv2.destroyAllWindows()
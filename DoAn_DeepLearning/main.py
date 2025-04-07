import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageEnhance, ImageTk, ImageFilter
import cv2  # Thư viện OpenCV để chụp ảnh
import numpy as np  # Thư viện NumPy để xử lý mảng

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Xử Lý Ảnh")

        self.image = None
        self.original_image = None

        # Nút tải ảnh
        self.load_button = tk.Button(root, text="Tải Ảnh", command=self.load_image)
        self.load_button.pack()

        # Nút chụp ảnh
        self.capture_button = tk.Button(root, text="Chụp Ảnh", command=self.capture_image)
        self.capture_button.pack()

        # Thanh điều chỉnh độ sắc nét
        self.sharpness_scale = tk.Scale(root, from_=1.0, to=5.0, resolution=0.1, orient=tk.HORIZONTAL, label="Độ Sắc Nét")
        self.sharpness_scale.set(1.0)  # Giá trị mặc định
        self.sharpness_scale.pack()

        # Thanh điều chỉnh độ sáng
        self.brightness_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Độ Sáng")
        self.brightness_scale.set(1.0)  # Giá trị mặc định
        self.brightness_scale.pack()

        # Thanh điều chỉnh độ tương phản
        self.contrast_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Độ Tương Phản")
        self.contrast_scale.set(1.0)  # Giá trị mặc định
        self.contrast_scale.pack()

        # Thanh điều chỉnh độ bão hòa
        self.saturation_scale = tk.Scale(root, from_=0.5, to=2.0, resolution=0.1, orient=tk.HORIZONTAL, label="Độ Bão Hòa")
        self.saturation_scale.set(1.0)  # Giá trị mặc định
        self.saturation_scale.pack()

        # Thanh điều chỉnh độ mờ
        self.blur_scale = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, label="Độ Mờ")
        self.blur_scale.set(0)  # Giá trị mặc định
        self.blur_scale.pack()

        # Nút áp dụng
        self.apply_button = tk.Button(root, text="Áp Dụng", command=self.apply_changes)
        self.apply_button.pack()

        # Nút lưu ảnh
        self.save_button = tk.Button(root, text="Lưu Ảnh", command=self.save_image)
        self.save_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.image = self.original_image.copy()  # Khởi tạo ảnh sửa đổi từ bản gốc
            self.process_image()  # Khử nhiễu và tăng cường độ nét ngay khi tải ảnh
            self.show_result_image()  # Hiển thị ảnh đã xử lý

    def capture_image(self):
        # Mở webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Lỗi", "Không thể mở webcam.")
            return

        ret, frame = cap.read()
        cap.release()  # Đóng webcam

        if ret:
            # Chuyển đổi từ BGR sang RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(frame)
            self.image = self.original_image.copy()  # Khởi tạo ảnh sửa đổi từ bản gốc
            self.process_image()  # Khử nhiễu và tăng cường độ nét ngay khi chụp ảnh
            self.show_result_image()  # Hiển thị ảnh đã chụp

    def process_image(self):
        # Chuyển đổi ảnh sang định dạng numpy để khử nhiễu
        img_array = cv2.cvtColor(np.array(self.image), cv2.COLOR_RGB2BGR)
        # Khử nhiễu bằng phương pháp Non-local Means Denoising
        img_array = cv2.fastNlMeansDenoisingColored(img_array, None, 10, 10, 7, 21)
        # Chuyển đổi lại sang định dạng PIL
        self.image = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
        # Tăng cường độ sắc nét cho ảnh
        sharpness = ImageEnhance.Sharpness(self.image)
        self.image = sharpness.enhance(2.0)  # Đặt độ sắc nét cao

    def apply_changes(self):
        if self.image is None:
            messagebox.showerror("Lỗi", "Vui lòng tải ảnh trước!")
            return

        # Áp dụng các điều chỉnh
        sharpness = ImageEnhance.Sharpness(self.image)
        self.image = sharpness.enhance(self.sharpness_scale.get())

        brightness = ImageEnhance.Brightness(self.image)
        self.image = brightness.enhance(self.brightness_scale.get())

        contrast = ImageEnhance.Contrast(self.image)
        self.image = contrast.enhance(self.contrast_scale.get())

        saturation = ImageEnhance.Color(self.image)
        self.image = saturation.enhance(self.saturation_scale.get())

        # Độ mờ (Blur)
        blur_radius = self.blur_scale.get()
        if blur_radius > 0:
            self.image = self.image.filter(ImageFilter.GaussianBlur(blur_radius))

        # Hiện thị ảnh trong cửa sổ mới
        self.show_result_image()

    def show_result_image(self):
        result_window = tk.Toplevel(self.root)
        result_window.title("Ảnh Đã Chỉnh Sửa")

        # Hiển thị ảnh trong cửa sổ mới
        tk_image = ImageTk.PhotoImage(self.image)
        result_label = tk.Label(result_window, image=tk_image)
        result_label.image = tk_image  # Giữ tham chiếu đến ảnh
        result_label.pack()

    def save_image(self):
        if self.image is None:
            messagebox.showerror("Lỗi", "Không có ảnh để lưu!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            self.image.save(file_path)
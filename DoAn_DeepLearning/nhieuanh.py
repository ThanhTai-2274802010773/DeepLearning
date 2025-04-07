import cv2
import numpy as np

def add_gaussian_noise(image, mean=0, sigma=25):
  """Thêm nhiễu Gaussian vào ảnh."""
  row, col, ch = image.shape
  gauss = np.random.normal(mean, sigma, (row, col, ch))
  gauss = gauss.reshape(row, col, ch)
  noisy = image + gauss
  noisy = np.clip(noisy, 0, 255).astype(np.uint8)
  return noisy

# Đọc ảnh
img = cv2.imread('your_image.jpg')#Thêm đường dẫn của ảnh muốn làm nhiễu

# Thêm nhiễu Gaussian
noisy_img = add_gaussian_noise(img)

# Hiển thị ảnh gốc và ảnh bị nhiễu
cv2.imshow('Original Image', img)
cv2.imshow('Gaussian Noise Image', noisy_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Lưu ảnh bị nhiễu
cv2.imwrite('input1.jpg', noisy_img)#chạy code xong bấm esc, muốn làm nhiễu thêm ảnh khác thì đổi số 1 thành số khác
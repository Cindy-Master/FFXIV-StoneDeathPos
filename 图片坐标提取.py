import cv2
import numpy as np

image_path = 'image.png'  
image = cv2.imread(image_path)
if image is None:
    print(f"无法读取图像：{image_path}")
    exit()
height, width = image.shape[:2]
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
flipped_contours = []
for contour in contours:
    new_contour = []
    for point in contour:
        x, y = point[0]
        flipped_y = height - y  
        #对于简单图案建议提高偏移量(例如：-5, 6)
        offset_x = np.random.randint(-2, 3)
        offset_y = np.random.randint(-2, 3)
        new_contour.append([[x + offset_x, flipped_y + offset_y]])
    new_contour = np.array(new_contour, dtype=np.int32)
    flipped_contours.append(new_contour)
output_file = 'contours_coordinates.txt'
with open(output_file, 'w') as f:
    for i, contour in enumerate(flipped_contours):
        f.write(f"Contour {i + 1}:\n")
        for point in contour:
            x, y = point[0]
            f.write(f"({x}, {y})\n")
        f.write("\n")
print(f"所有轮廓坐标已保存到 {output_file}")
flipped_image = cv2.flip(image, 0)
cv2.drawContours(flipped_image, flipped_contours, -1, (0, 255, 0), 2)
cv2.imshow('Contours', flipped_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

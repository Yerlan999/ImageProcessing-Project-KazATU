import numpy as np
import cv2


h = 30
path = '29.jpg'

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 0.5
color = (0, 0, 255)
thickness = 1

img = cv2.imread(path)

imgDenoised = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
blur = cv2.bilateralFilter(imgDenoised, 7, 11, 11)

gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
ret, th = cv2.threshold(gray, 20, 255,
                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)


unique, counts = np.unique(th, return_counts=True)
result = dict(zip(unique, counts))

num_white_pixels = result[255]
img_height, img_width, _ = img.shape
max_pixel_count = img_width * img_height
relational_pixel_count = num_white_pixels / max_pixel_count
org = (10, img_height - 10)

cv2.putText(img, path.split(".")[0] + ' ' + str(num_white_pixels), org, font,
            fontScale, color, thickness, cv2.LINE_AA)

#0.00000467146609973919 * (h**2) - 0.000365097778525 * h + 0.007668397174133
print("Debug: ", relational_pixel_count)
real_cm2 = round((relational_pixel_count / (0.00000467146609973919 *
                                            (h**2) - 0.000365097778525 * h + 0.007668397174133)), 2)
#corrected_real_cm2 = real_cm2 - real_cm2 * 0.10

print("Done!")
cv2.imwrite("result.jpg", img)
cv2.imwrite("result_thres.jpg", th)
print(real_cm2)

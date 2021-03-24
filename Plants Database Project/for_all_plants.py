from datetime import datetime
import pandas as pd
import numpy as np
import cv2
import os


# FUNCTION FOR CORRECTION BY PIXELS
def correction_basedOnPixels(num_white_pixels, max_pixel_count):
    corr_percent = round((num_white_pixels / max_pixel_count) * 100)
    correction_coeff = corr_percent / 57.14
    num_white_pixels = num_white_pixels - num_white_pixels * correction_coeff
    return num_white_pixels


# GENERAL DATASTRUCTURE NEEDED
current_dir = os.getcwd()
total_area = 0
biggest_area = {
    "area": 0,
    "contour": None,
}


# ITERATE FOR EACH JPEG FILE IN CURRENT DIRECTORY
for filename in os.listdir(current_dir):
    if filename.endswith("w.jpg"):
        # HEIGHT AND FILE NAME
        # h = 23
        path = filename

        # FONT PROPERTIES
        font = cv2.FONT_HERSHEY_SIMPLEX
        fontScale = 0.5
        color = (0, 0, 255)
        thickness = 1

        # READ IMAGE AND GET BASIC INFORMATION
        original_img = cv2.imread(path)
        img_height, img_width, _ = original_img.shape
        max_pixel_count = img_width * img_height

        # APPLYING FILTERS AND GETTING RAW IMAGES
        imgDenoised = cv2.fastNlMeansDenoisingColored(
            original_img, None, 10, 10, 7, 21)                       # INPUT <----
        imgGreenChannel = imgDenoised[:, :, 1]
        edges = cv2.Canny(imgGreenChannel, 100, 200)
        blur = cv2.bilateralFilter(imgGreenChannel, 7, 11, 11)
        ret, th = cv2.threshold(blur, 130, 255,
                                cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        dilated = cv2.dilate(edges, kernel)
        eroded = cv2.erode(dilated, kernel)


        # INVERTING BLACK AND WHITE COLORS
        inverted_thresh = 255 - th                               # OUTPUT ---->


        # FINDING CONTOURS !
        contours, hierarchy = cv2.findContours(
            eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(original_img, contours, -1, (255, 0, 0), 1)


        # CALCULATING AREA AND PUTTING THEM ON IMAGE
        for cnt in contours:

            area = cv2.contourArea(cnt)
            if area > biggest_area["area"]:
                biggest_area["area"] = area
                biggest_area["contour"] = cnt
            total_area += area
            M = cv2.moments(cnt)

            try:
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
            except ZeroDivisionError:
                continue

            cv2.putText(original_img, str(area), (cx, cy), font,
                        fontScale, color, thickness, cv2.LINE_AA)


        cv2.putText(original_img, str(total_area), (50, 50), font,
                    fontScale, (255, 255, 0), 2, cv2.LINE_AA)


        # APPLYING CONVEX HULL METHOD
        hull = cv2.convexHull(biggest_area["contour"])
        cv2.drawContours(original_img, [hull], 0, (0, 0, 255), 2)


        # EXTRACT ONLY INTERNAL AREA OF THE HULL
        stencil = np.zeros(inverted_thresh.shape).astype(original_img.dtype)
        color = [255, 255, 255]
        cv2.fillPoly(stencil, [hull], color)
        result = cv2.bitwise_and(inverted_thresh, stencil)


        # COUNTING NUMBER OF WHITE PIXELS
        unique, counts = np.unique(result, return_counts=True)
        result_dict = dict(zip(unique, counts))
        num_white_pixels = result_dict[255]


        # APPLYING SOME CORRECTION
        # num_white_pixels = correction_basedOnPixels(num_white_pixels, max_pixel_count)


        # GETTING RELATION BETWEEN ALL PIXELS AND WHITE PIXELS
        relational_pixel_count = (num_white_pixels / max_pixel_count) * 100
        org = (10, img_height - 10)


        # POLYNOMIAL FORMULA TO CALCULATE REAL AREA BASED ON NUMBER OF WHITE PIXELS !!!!
        # real_cm2 = round((relational_pixel_count / (0.00000467146609973919 *
        #                                             (h**2) - 0.000365097778525 * h + 0.007668397174133)), 2)


        # PRINTING AND SHOWING RESULTS
        cv2.imwrite("result_thresholds/" + "threshold_" + filename, result)           # <--- HULL EXTRACTED
        # cv2.imwrite("thres.jpg", inverted_thresh)   # <--- INVERTED THRESHOLD
        # cv2.imwrite('test.jpg', original_img)       # <--- ORIGINAL IMAGE

        # print("Real area(calculated):", real_cm2)
        # print("Number of white pixels: ", num_white_pixels)


        # print("Done!")
        # LOGGING RESULTS INTO LOG FILE
        with open('log.txt', 'a') as file:
                plant_number = filename.split("w")[0]
                file.write(plant_number + " " + str(relational_pixel_count) + "\n")
                print("Done with " + filename + "!")

print("Process is complete!")

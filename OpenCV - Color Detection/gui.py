import os
import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import cv2


class MainWindow():
    def __init__(self, window, cap, list_of_hsv_vals):

        self.hue_min, self.sat_min, self.val_min, self.hue_max, self.sat_max, self.val_max = list_of_hsv_vals

        self.window = window
        self.cap = cap
        self.set_caps(900, 600)
        # Update image on canvas
        self.update_image()


    def set_caps(self, width, height):

        self.cap.set(3, width);
        self.cap.set(4, height);
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20 # Interval in ms to get the latest frame

        # Create canvas for image
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.place(x=0, y=0)

    def update_image(self):
        # Get the latest frame and convert image format
        self.image_org = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image_hsv = cv2.cvtColor(self.image_org, cv2.COLOR_BGR2HSV) # to RGB

        # self.image_filtered = cv2.bilateralFilter(self.image_hsv, 9, 75, 75)

        h_min = self.hue_min.get()
        s_min = self.sat_min.get()
        v_min = self.val_min.get()

        h_max = self.hue_max.get()
        s_max = self.sat_max.get()
        v_max = self.val_max.get()

        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(self.image_hsv, lower, upper)
        self.image_masked = cv2.bitwise_and(self.image_org, self.image_org, mask=mask)


        self.image_pil = Image.fromarray(self.image_masked) # to PIL format
        self.image_to_show = ImageTk.PhotoImage(self.image_pil) # to ImageTk format

        # Update image
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_to_show)

        # Repeat every 'interval' ms
        self.window.after(self.interval, self.update_image)


    def capture_image(self):
        print("Captured!")
        self.image_pil.save("test.jpg")

    def change_camera(self, cam_type):
        self.canvas.delete("all")

        if cam_type == 0:
            self.cap = cv2.VideoCapture(cam_type, cv2.CAP_DSHOW)
            self.set_caps(600, 600)

        if cam_type == 1:
            self.cap = cv2.VideoCapture(cam_type, cv2.CAP_DSHOW)
            self.set_caps(900, 600)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('1366x768')


    list_hsv_minmax = [h + "_" + m for m in ["min", "max"] for h in ["hue", "sat", "val"]]
    for var in list_hsv_minmax:
        exec(var + " = tk.IntVar()")

    cam_type = tk.IntVar()
    cam_type.set(1)

    for i, widget in enumerate(list_hsv_minmax):
        if widget.startswith("hue"):
            exec("widget = tk.Scale(root, from_=0, to=179, variable=" + widget + ", length=180, orient=tk.HORIZONTAL)")
        else:
            exec("widget = tk.Scale(root, from_=0, to=255, variable=" + widget + ", length=180, orient=tk.HORIZONTAL)")
        widget.place(x=1100, y=40+(i*40))
        widget.set(100)

    list_of_hsv_vals = [hue_min, sat_min, val_min, hue_max, sat_max, val_max]

    win = MainWindow(root, cv2.VideoCapture(cam_type.get(), cv2.CAP_DSHOW), list_of_hsv_vals)


    rad_but_1 = tk.Radiobutton(root, text="Cam 1",padx = 5, font=("bold", 11), variable=cam_type,
        value=0, command=lambda:win.change_camera(0))
    rad_but_2 = tk.Radiobutton(root, text="Cam 2",padx = 5, font=("bold", 11), variable=cam_type,
        value=1, command=lambda:win.change_camera(1))
    rad_but_1.place(x=1000, y=530)
    rad_but_2.place(x=1000, y=560)




    capture_button = tk.Button(root, text ="Capture", command = win.capture_image)
    capture_button.place(x=1100, y=500)


    root.mainloop()
    os.system("taskkill /F /IM python3.8.exe /T")

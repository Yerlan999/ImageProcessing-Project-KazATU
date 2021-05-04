import os, re, threading, cv2
import tkinter as tk
from tkinter.ttk import Progressbar
from tkinter import messagebox, HORIZONTAL, END
import numpy as np
from PIL import Image, ImageTk
from datetime import datetime


calc_button_color_1 = "#006400"
calc_button_color_2 = "#004b23"

font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 255, 0)
thickness = 1



def validate_numbers(index, numbers):
    global pattern
    return pattern.match(numbers) is not None


class MainWindow():
    def __init__(self, window, cap, list_of_hsv_vals):

        self.hue_min, self.sat_min, self.val_min, self.hue_max, self.sat_max, self.val_max = list_of_hsv_vals

        self.window = window
        self.cap = cap
        self.set_caps(900, 600)
        # Update image on canvas
        self.update_image()
        self.capture_button = tk.Button(root, text ="Рассчитать", width=30, bg=calc_button_color_1,
        fg='white', height=2, activebackground=calc_button_color_2, command=lambda:win.capture_image_wrapper(height_from_plant))
        self.capture_button.place(x=1100, y=600)


    def set_caps(self, width, height):

        self.cap.set(3, width);
        self.cap.set(4, height);
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.interval = 20 # Interval in ms to get the latest frame

        # Create canvas for image
        self.canvas = tk.Canvas(self.window, width=self.width, height=self.height)
        self.canvas.place(x=30, y=40)

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

    def capture_image_wrapper(self, height_from_plant):
        answer = messagebox.askyesno(title="Расчет", message="Вы уверены что хотите произвести раcчет по указанным данным?")
        if answer == False: return;
        try:
            height_from_plant = float(height_from_plant.get())
        except:
            messagebox.showerror(title="Ошибка!", message="Введите значение высоты камеры от растения")
            return

        def capture_image():

            progress_pivot = (1100,570)
            progress_bar = Progressbar(root, orient=HORIZONTAL,length=218,  mode='indeterminate')
            progress_bar.place(x=progress_pivot[0], y=progress_pivot[1])
            progress_bar_label = tk.Label(root, text="Обработка данных...", font=("bold", 10))
            progress_bar_label.place(x=progress_pivot[0], y=progress_pivot[1]-30)

            self.capture_button["state"] = "disabled"
            progress_bar.start()

            # img = cv2.imread("SampleImages/nursery.jpg")

            # REAL IMAGE
            open_cv_image = np.array(self.image_pil)
            img = open_cv_image[:, :, ::-1].copy()

            img_height, img_width, _ = img.shape
            max_pixel_count = img_width * img_height

            imgDenoisedColored = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
            imgGreenChannel = imgDenoisedColored[:,:,1]
            imgDenoisedFinal = cv2.fastNlMeansDenoising(imgGreenChannel, 10, 10, 7, 21)

            blur = cv2.bilateralFilter(imgDenoisedFinal,7,11,11)
            ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            kernel = np.ones((5,5),np.uint8)
            opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

            unique, counts = np.unique(closing, return_counts=True)
            result = dict(zip(unique, counts))
            num_white_pixels = result[255]*1.3


            relational_pixel_count = (num_white_pixels / max_pixel_count) * 100
            org = (10, img_height - 10)

            real_cm2 = round((relational_pixel_count / (4.17277589255267 - 0.277111499290506*(height_from_plant**1) - 0.0153889344192674*(height_from_plant**2) + 0.00232991009995106*(height_from_plant**3) - 0.0000993963917490068*(height_from_plant**4) + 1.87433703715374E-06*(height_from_plant**5) - 1.34236754826271E-08*(height_from_plant**6))), 2)

            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")

            cv2.putText(img, str(real_cm2) + ' cm2. ' + str(current_datetime), org, font,
                               fontScale, color, thickness, cv2.LINE_AA)

            name_of_file = str(current_datetime).replace("/", "-").replace(":", "-").replace(" ", "_")

            cv2.imwrite(name_of_file + '_white_black.jpg', th)
            cv2.imwrite(name_of_file + '_original.jpg', img)
            # cv2.imshow(name_of_file + '_white_black.jpg', th)
            # cv2.imshow(name_of_file + '_original.jpg', img)
            progress_bar.stop()
            self.capture_button["state"] = "normal"
            progress_bar_label.destroy()
            progress_bar.destroy()
            messagebox.showinfo(title="Расчет завершен!", message="Данные успешно обработаны!")

        threading.Thread(target=capture_image).start()


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
    cam_type.set(0)

    height_from_plant = tk.StringVar()


    plant_height_label = tk.Label(root, text="Расчет площади растения", font=("bold", 20))
    plant_height_label.place(x=950, y=50)


    hsv_pivot = (1100, 130)
    for i, widget in enumerate(list_hsv_minmax):
        if widget.startswith("hue"):
            exec("widget = tk.Scale(root, from_=0, to=179, variable=" + widget + ", length=180, orient=tk.HORIZONTAL)")
        else:
            exec("widget = tk.Scale(root, from_=0, to=255, variable=" + widget + ", length=180, orient=tk.HORIZONTAL)")
        widget.place(x=hsv_pivot[0], y=hsv_pivot[1]+(i*40))
        widget.set(100)

    list_of_hsv_vals = [hue_min, sat_min, val_min, hue_max, sat_max, val_max]



    list_hsv_minmax_label = [hsv + " " + mm for mm in ["мин", "макс"] for hsv in ["Тон", "Насыщенность", "Яркость"]]
    for i, label in enumerate(list_hsv_minmax_label):
        tk.Label(root, text=label, font=("bold", 11)).place(x=hsv_pivot[0]-200, y=hsv_pivot[1]+20+(i*40))



    try:
        win = MainWindow(root, cv2.VideoCapture(cam_type.get(), cv2.CAP_DSHOW), list_of_hsv_vals)
    except:
        messagebox.showerror(title="Ошибка!", message="Камера подключена неправильно")
        root.destroy()

    rad_button_pivot = (30, 10)
    tk.Label(root, text="Выбор камеры:", font=("bold", 12)).place(x=rad_button_pivot[0], y=rad_button_pivot[1])
    rad_but_1 = tk.Radiobutton(root, text="Основная веб-камера",padx = 5, font=("bold", 11), variable=cam_type,
        value=0, command=lambda:win.change_camera(0))
    rad_but_2 = tk.Radiobutton(root, text="Подключенная камера",padx = 5, font=("bold", 11), variable=cam_type,
        value=1, command=lambda:win.change_camera(1))
    rad_but_1.place(x=rad_button_pivot[0]+200, y=rad_button_pivot[1])
    rad_but_2.place(x=rad_button_pivot[0]+400, y=rad_button_pivot[1])

    pattern = re.compile(r'^([\.\d]*)$')
    vcmd = (root.register(validate_numbers), "%i", "%P")
    plant_height_label = tk.Label(root, text="Высота до растения в (см)", font=("bold", 11))
    plant_height_label.place(x=hsv_pivot[0]-200, y=hsv_pivot[1]+269)

    plant_height_entry = tk.Entry(root, textvariable=height_from_plant, width=29, validate="key", validatecommand=vcmd)
    plant_height_entry.place(x=hsv_pivot[0]+3, y=hsv_pivot[1]+270)


    root.mainloop()
    os.system("taskkill /F /IM python3.8.exe /T")

from tkinter import messagebox, HORIZONTAL, END, DISABLED, filedialog
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import tkinter.font as tkFont
import os, re, threading, cv2
from datetime import datetime
import tkinter as tk
import numpy as np
from pathlib import Path


calc_button_color_1 = "#6a040f"
calc_button_color_2 = "#370617"
window_color = entry_color = "#003566"
text_color = "#ffffff"
s_entry_color = "#dad7cd"
s_text_color = "#000000"
e_entry_color = "#ebf2fa"
troughcolor = "#ebf2fa"


font = cv2.FONT_HERSHEY_SIMPLEX
fontScale = 1
color = (0, 255, 0)
thickness = 1



class Cheating():
    def __init__(self, image):
        self.image = image

    def read(self):
        return (0, self.image)


def validate_numbers(index, numbers):
    global pattern
    return pattern.match(numbers) is not None


class MainWindow():
    def __init__(self, window, cap, list_of_hsv_vals):

        self.hue_min, self.sat_min, self.val_min, self.hue_max, self.sat_max, self.val_max = list_of_hsv_vals
        self.window = window
        self.cap = cap

        if self.cap != "Only Images":
            self.set_caps("Video Streaming", 801, 601)
            # Update image on canvas
            self.update_image()
        else:
            self.canvas = tk.Canvas(self.window, width=800, height=600 , bg=window_color, highlightbackground=window_color)
            self.canvas.place(x=30, y=40)
            self.interval = 20
            self.no_camera = True


        self.capture_button = tk.Button(root, text ="Рассчитать", font=helv10, width=25, bg=calc_button_color_1,
        fg='white', height=2, activebackground=calc_button_color_2, command=lambda:win.capture_image_wrapper(height_from_plant))
        self.capture_button.place(x=1000, y=600)

        self.label_picture = tk.Label(root, text="Путь к фотоке:",width=20,font=("bold", 12))
        self.label_picture.place(x=895,y=450)

        self.picture_path = tk.Entry(root, font=30)
        self.picture_path.grid(row=2,column=6)
        self.picture_path.place(x=2000,y=2000)


        self.select_button_pic = tk.Button(root,text="Выбрать",font=40, command=self.choose_picture).place(x=1105,y=445)


    def set_caps(self, mode, width, height):

        if mode == "Video Streaming":
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            # Create canvas for image
            self.canvas = tk.Canvas(self.window, width=self.width, height=self.height , bg=window_color, highlightbackground=window_color)
            self.canvas.place(x=30, y=40)
        else:
            image_height, image_width, _ = self.image_org.shape
            self.canvas = tk.Canvas(self.window, width=image_width, height=image_height, bg=window_color, highlightbackground=window_color)
            self.canvas.place(x=30, y=40)
        self.interval = 20 # Interval in ms to get the latest frame


    def update_image(self):

        self.image_org = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB) # to RGB
        self.image_hsv = cv2.cvtColor(self.image_org, cv2.COLOR_RGB2HSV) # to RGB


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

        self.window.after(self.interval, lambda:self.update_image())


    def capture_image_wrapper(self, height_from_plant):
        answer = messagebox.askyesno(title="Расчет", message="Вы уверены что хотите произвести раcчет по указанным данным?")
        if answer == False: return;
        try:
            height_from_plant = float(height_from_plant.get())
        except:
            messagebox.showerror(title="Ошибка!", message="Введите значение высоты камеры от растения")
            return

        def capture_image():

            progress_pivot = (1000,570)
            progress_bar = Progressbar(root, orient=HORIZONTAL,length=232,  mode='indeterminate')
            progress_bar.place(x=progress_pivot[0], y=progress_pivot[1])
            progress_bar_label = tk.Label(root, text="Обработка данных...", font=helv10, bg=entry_color, fg=text_color)
            progress_bar_label.place(x=progress_pivot[0], y=progress_pivot[1]-30)

            self.capture_button["state"] = "disabled"
            progress_bar.start()

            # REAL IMAGE
            open_cv_image = np.array(self.image_pil)
            img = open_cv_image[:, :, ::-1].copy()

            img_height, img_width, _ = img.shape
            max_pixel_count = img_width * img_height

            imgDenoisedColored = cv2.fastNlMeansDenoisingColored(img, None, 15, 15, 7, 21)
            imgGreenChannel = imgDenoisedColored[:,:,1]
            imgDenoisedFinal = cv2.fastNlMeansDenoising(imgGreenChannel, 15, 15, 7, 21)

            blur = cv2.bilateralFilter(imgDenoisedFinal,7,15,15)
            ret,th = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

            kernel = np.ones((10,10),np.uint8)
            opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel)
            closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)

            unique, counts = np.unique(closing, return_counts=True)
            result = dict(zip(unique, counts))
            num_white_pixels = result[255]*1.4


            relational_pixel_count = (num_white_pixels / max_pixel_count) * 100
            org = (10, img_height - 10)

            real_cm2 = round((relational_pixel_count / (4.17277589255267 - 0.277111499290506*(height_from_plant**1) - 0.0153889344192674*(height_from_plant**2) + 0.00232991009995106*(height_from_plant**3) - 0.0000993963917490068*(height_from_plant**4) + 1.87433703715374E-06*(height_from_plant**5) - 1.34236754826271E-08*(height_from_plant**6))), 2)

            current_datetime = datetime.now().strftime("%d/%m/%Y %H:%M")

            cv2.putText(img, str(real_cm2) + ' cm2. ' + str(current_datetime), org, font,
                               fontScale, color, thickness, cv2.LINE_AA)

            name_of_file = str(current_datetime).replace("/", "-").replace(":", "-").replace(" ", "_")

            cv2.imwrite(name_of_file + '_white_black.jpg', th)
            cv2.imwrite(name_of_file + '_original.jpg', img)

            progress_bar.stop()
            self.capture_button["state"] = "normal"
            progress_bar_label.destroy()
            progress_bar.destroy()
            messagebox.showinfo(title="Расчет завершен!", message="Данные успешно обработаны!")

        threading.Thread(target=capture_image).start()


    def change_camera(self, cam_type):
        self.canvas.delete("all")

        if cam_type == 0:
            try:
                self.cap = cv2.VideoCapture(cam_type, cv2.CAP_DSHOW)
                self.set_caps("Video Streaming", 801, 601)
            except:
                messagebox.showerror(title="Ошибка!", message="Камера подключена неправильно")
                return
        if cam_type == 1:
            try:
                self.cap = cv2.VideoCapture(cam_type, cv2.CAP_DSHOW)
                self.set_caps("Video Streaming", 801, 601)
            except:
                messagebox.showerror(title="Ошибка!", message="Камера подключена неправильно")
                return

    def choose_picture(self):

        self.canvas.delete("all")
        filename = filedialog.askopenfilename(filetypes=[("Pictures", ".jpeg .png  .jpg"), ("ALL","*.*")])
        self.picture_path.insert(END, filename) # add this
        picture = Path(self.picture_path.get())

        self.image_org = cv2.imread(str(picture))
        self.image_org = cv2.resize(self.image_org, (800, 600), interpolation = cv2.INTER_AREA)

        self.cap = Cheating(self.image_org)
        self.set_caps("Only Images", 801, 601)

        self.picture_path.delete(0, 'end')
        if self.no_camera:
            self.no_camera = False
            self.update_image()


if __name__ == "__main__":
    try:
        root = tk.Tk()

        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        root.geometry('%dx%d+0+0' % (width,height))
        root.configure(bg=window_color)
        helv21 = tkFont.Font(family="Georgia",size=21,weight="bold")
        helv10 = tkFont.Font(family="Georgia",size=10,weight="bold")
        helv11 = tkFont.Font(family="Georgia",size=11,weight="bold")
        helv12 = tkFont.Font(family="Georgia",size=12,weight="bold")

        list_hsv_minmax = [h + "_" + m for m in ["min", "max"] for h in ["hue", "sat", "val"]]
        for var in list_hsv_minmax:
            exec(var + " = tk.IntVar()")

        cam_type = tk.IntVar()
        cam_type.set(0)

        height_from_plant = tk.StringVar()


        plant_height_label = tk.Label(root, text="Расчет площади растения", font=helv21, bg=s_entry_color, fg=s_text_color)
        plant_height_label.place(x=900, y=50)


        hsv_pivot = (1100, 130)
        for i, widget in enumerate(list_hsv_minmax):
            if widget.startswith("hue"):
                exec("widget = tk.Scale(root, from_=0, to=179, variable=" + widget + ", length=180, orient=tk.HORIZONTAL, bg=s_entry_color, fg=s_text_color, troughcolor=troughcolor)")
            else:
                exec("widget = tk.Scale(root, from_=0, to=255, variable=" + widget + ", length=180, orient=tk.HORIZONTAL, bg=s_entry_color, fg=s_text_color, troughcolor=troughcolor)")
            widget.place(x=hsv_pivot[0], y=hsv_pivot[1]+(i*40))


        hue_min.set(0); hue_max.set(179);
        sat_min.set(0); sat_max.set(255);
        val_min.set(0); val_max.set(255);


        list_of_hsv_vals = [hue_min, sat_min, val_min, hue_max, sat_max, val_max]



        list_hsv_minmax_label = [hsv + " " + mm for mm in ["мин", "макс"] for hsv in ["Тон", "Насыщенность", "Яркость"]]
        for i, label in enumerate(list_hsv_minmax_label):
            tk.Label(root, text=label, font=helv11, bg=entry_color, fg=text_color).place(x=hsv_pivot[0]-200, y=hsv_pivot[1]+20+(i*40))


        webcam_broken= None
        addcamera_broken = None

        try:
            test = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            test.set(cv2.CAP_PROP_FRAME_WIDTH, 801)
            test.set(cv2.CAP_PROP_FRAME_HEIGHT, 601)
            if test.get(cv2.CAP_PROP_FRAME_WIDTH) == 801 and test.set(cv2.CAP_PROP_FRAME_HEIGHT) == 601:
                raise ValueError

        except:
            webcam_broken = True
        try:
            test = cv2.VideoCapture(1, cv2.CAP_DSHOW)
            test.set(cv2.CAP_PROP_FRAME_WIDTH, 801)
            test.set(cv2.CAP_PROP_FRAME_HEIGHT, 601)
            if test.get(cv2.CAP_PROP_FRAME_WIDTH) == 801 and test.set(cv2.CAP_PROP_FRAME_HEIGHT) == 601:
                raise ValueError

        except:
            addcamera_broken = True


        if webcam_broken and addcamera_broken:
            messagebox.showerror(title="Ошибка!", message="Не удалось найти доступное устройство")
            win = MainWindow(root, "Only Images", list_of_hsv_vals)
        elif not webcam_broken and addcamera_broken:
            win = MainWindow(root, cv2.VideoCapture(0, cv2.CAP_DSHOW), list_of_hsv_vals)
            cam_type.set(0)
        elif not addcamera_broken and webcam_broken:
            win = MainWindow(root, cv2.VideoCapture(1, cv2.CAP_DSHOW), list_of_hsv_vals)
            cam_type.set(1)
        elif not addcamera_broken and not webcam_broken:
            win = MainWindow(root, cv2.VideoCapture(1, cv2.CAP_DSHOW), list_of_hsv_vals)
            cam_type.set(1)


        rad_button_pivot = (30, 10)

        tk.Label(root, text="Выбор камеры:", font=helv12, bg=entry_color, fg=text_color).place(x=rad_button_pivot[0], y=rad_button_pivot[1])
        tk.Label(root, text="Основная веб-камера", font=helv12, bg=entry_color, fg=text_color).place(x=rad_button_pivot[0]+190, y=rad_button_pivot[1])
        tk.Label(root, text="Подключенная камера", font=helv12, bg=entry_color, fg=text_color).place(x=rad_button_pivot[0]+430, y=rad_button_pivot[1])
        rad_but_1 = tk.Radiobutton(root, padx = 5, font=helv11, variable=cam_type,
            value=0, command=lambda:win.change_camera(0), bg=entry_color, fg="#000000")
        rad_but_2 = tk.Radiobutton(root, padx = 5, font=helv11, variable=cam_type,
            value=1, command=lambda:win.change_camera(1), bg=entry_color, fg="#000000")
        rad_but_1.place(x=rad_button_pivot[0]+150, y=rad_button_pivot[1])
        rad_but_2.place(x=rad_button_pivot[0]+390, y=rad_button_pivot[1])

        if webcam_broken:
            rad_but_1.configure(state = DISABLED)
        if addcamera_broken:
            rad_but_2.configure(state = DISABLED)


        pattern = re.compile(r'^([\.\d]*)$')
        vcmd = (root.register(validate_numbers), "%i", "%P")
        plant_height_label = tk.Label(root, text="Высота до растения в (см)", font=helv11, bg=entry_color, fg=text_color)
        plant_height_label.place(x=hsv_pivot[0]-220, y=hsv_pivot[1]+269)

        plant_height_entry = tk.Entry(root, textvariable=height_from_plant, width=29, validate="key", validatecommand=vcmd, bg=e_entry_color)
        plant_height_entry.place(x=hsv_pivot[0]+3, y=hsv_pivot[1]+270)


        root.mainloop()
    finally:
        os.system("taskkill /F /IM python3.8.exe /T")

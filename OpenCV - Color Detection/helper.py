from tkinter import *
import os


def donothing():
    pass

def main_properties(main_frame):

    Label(main_frame, text="Main Title", width=55, height=2, borderwidth=2, relief="groove",font=("bold", 13)).grid(row=0, column=0, columnspan=3, sticky="EWNS")

    for i, (_, label, var, ed_iz) in enumerate(main_entry_list_names, start=1):

        if ed_iz:
            Label(main_frame, text=label, width=25, height=2, borderwidth=2, relief="groove",font=("bold", 11)).grid(row=i, column=0, sticky="EWNS")
            Entry(main_frame, width=40).grid(row=i, column=1, sticky="EWNS")
            OptionMenu(main_frame, eval(var), *ed_iz).grid(row=i, column=2, sticky="EWNS")
        else:
            Label(main_frame, text=label, width=25, height=2, borderwidth=2, relief="groove",font=("bold", 11)).grid(row=i, column=0, sticky="EWNS")
            Entry(main_frame, width=40).grid(row=i, column=1, sticky="EWNS")

    main_frame.pack(side=LEFT, anchor=E, fill=BOTH, expand=True)



def xy_properties(main_frame, xy_frame):
    main_frame.pack_forget()

    Label(xy_frame, text="Main Title", width=90, height=2, borderwidth=2, relief="groove",font=("bold", 13)).grid(row=0, column=0, columnspan=4, sticky="EWNS")
    for i, num in enumerate(range(0,14), start=1):
        Label(xy_frame, text="Test", width=40, height=2, borderwidth=2, relief="groove",font=("bold", 11)).grid(row=i, column=0, sticky="EWNS")
        Entry(xy_frame, width=15).grid(row=i, column=1, sticky="EWNS")
        Button(xy_frame, text="Test").grid(row=i, column=2, sticky="EWNS")
        Button(xy_frame, text="Test").grid(row=i, column=3, sticky="EWNS")



    xy_frame.pack(side=LEFT, anchor=E, fill=BOTH, expand=True)


root = Tk()
# root.resizable(0, 1)
root.geometry("540x460+20+20")

main_frame = Frame(root)
main_frame.rowconfigure(list(range(0,11)), weight=2)
main_frame.columnconfigure(list(range(0,3)), weight=1)


xy_frame = Frame(root)
xy_frame.rowconfigure(list(range(0,11)), weight=2)
# xy_frame.columnconfigure(list(range(0,4)), weight=1)
xy_frame.columnconfigure(0, weight=5)
xy_frame.columnconfigure(1, weight=1)
xy_frame.columnconfigure(2, weight=1)
xy_frame.columnconfigure(3, weight=1)



menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Main Settings", command=lambda:main_properties(main_frame))
filemenu.add_command(label="XY Coordinates", command=lambda:xy_properties(main_frame, xy_frame))
filemenu.add_command(label="Line Properties", command=donothing)
filemenu.add_separator()
filemenu.add_command(label="Calculate", command=root.quit)
menubar.add_cascade(label="Properties", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

root.config(menu=menubar)


main_entry_list_names = [
        ("inp_name_podstans", "Наименование подстанции", "", ()),
        ("inp_name_prisoedin", "Наименования присоед-ии", "", ()),
        ("inp_kolich_prisoed", "Количество присоед.", "", ()),
        ("inp_dlina_linii", "Длина линии", 'dlina_edin_izmer', ("м", "км")),
        ("inp_kolich_izmer", "Количество измерении", "", ()),
        ("inp_interval_izmer", "Интервал измерении", 'inter_izmer_edin_izmer', ("сек", "мин")),
        ("inp_kolich_garmonik", "Количество гармоник", "", ()),
        ("inp_napryazhen_linii", "Напряжение линии", 'naprzh_linii_edin_izmer', ("В", "кВ")),
]; main_entry_list_vars = []


for main_var, *rest in main_entry_list_names:
        exec(main_var + "=StringVar(main_frame)")
        main_entry_list_vars.append(eval(main_var))

# ("См/м", "кСм/м", "МСм/м")   ("мм\u00b2", "см\u00b2", "м\u00b2")

edin_imzer_list_names =[
    ('dlina_edin_izmer', 'км'),
    ('inter_izmer_edin_izmer', 'мин'),
    ('naprzh_linii_edin_izmer', 'кВ'),
    ('gamma_edin_izmer ', 'МСм/м'),
    ('pop_sech_edin_izmer', 'мм\u00b2'),
]; edin_imzer_list_vars = []


for main_var, def_val in edin_imzer_list_names:
    exec(main_var + "=StringVar(main_frame)")
    eval(main_var).set(def_val)
    edin_imzer_list_vars.append(eval(main_var))



root.mainloop()
os.system("taskkill /F /IM python3.8.exe /T")

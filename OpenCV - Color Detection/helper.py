from tkinter import *
import os
root = Tk()
root.geometry("700x300+500+100")

frame = Frame(root)


main_entry_list_names = [
        ("inp_name_podstans", "Наименование подстанции", ()),
        ("inp_name_prisoedin", "Наименования присоед-ии", ()),
        ("inp_kolich_prisoed", "Количество присоед.", ()),
        ("inp_dlina_linii", "Длина линии", ("m", "km")),
        ("inp_kolich_izmer", "Количество измерении", ()),
        ("inp_interval_izmer", "Интервал измерении", ("sec", "min")),
        ("inp_kolich_garmonik", "Количество гармоник", ()),
        ("inp_napryazhen_linii", "Напряжение линии", ("kV")),
    ]

main_entry_list_vars = []

for main_var, *rest in main_entry_list_names:
        exec(main_var + "=StringVar()")
        main_entry_list_vars.append(eval(main_var))


'dlina_edin_izmer'
'inter_izmer_edin_izmer'
'naprzh_linii_edin_izmer'
'gamma_edin_izmer '
'pop_sech_edin_izmer



Label(frame, text="Main Title", width=85, height=2, borderwidth=2, relief="groove",font=("bold", 13)).grid(row=0, column=0, columnspan=3, sticky="EWNS")

dlina_edin_izmer = StringVar(frame)

for i, (_, label, ed_iz) in enumerate(main_entry_list_names, start=1):
    print(*ed_iz)
    if ed_iz:
        Label(frame, text=label, width=40, height=2, borderwidth=2, relief="groove",font=("bold", 11)).grid(row=i, column=0, sticky="EWNS")
        Entry(frame, width=40).grid(row=i, column=1, sticky="EWNS")
        OptionMenu(frame, dlina_edin_izmer, *ed_iz).grid(row=i, column=2, sticky="EWNS")
    else:
        Label(frame, text=label, width=40, height=2, borderwidth=2, relief="groove",font=("bold", 11)).grid(row=i, column=0, sticky="EWNS")
        Entry(frame, width=40).grid(row=i, column=1, sticky="EWNS")
        # Button(frame, text="Ed", width=5, height=2).grid(row=i, column=2, sticky="EWNS")

frame.pack(side=LEFT, anchor=E, fill=BOTH, expand=True)



mainloop()
os.system("taskkill /F /IM python3.8.exe /T")

import time
from psutil import cpu_percent, virtual_memory
from tkinter import *


def observer(q):
    observer_window = Tk()
    observer_window.attributes("-fullscreen", True)
    observer_window.configure(background='black')
    observer_window.title("Canario")
    observer_window.bind("x", quit)

    clock_label = Label(observer_window, font=('arial', 150, 'bold'), fg='yellow', bg='black')
    clock_label.pack()
    date_label = Label(observer_window, font=('arial', 75, 'bold'), fg='skyblue', bg='black')
    date_label.pack()
    cpu_label = Label(observer_window, font=('arial', 50, 'bold'), fg='skyblue', bg='black')
    cpu_label.pack()
    ram_label = Label(observer_window, font=('arial', 50, 'bold'), fg='skyblue', bg='black')
    ram_label.pack()

    def tick():
        current_time = time.strftime('%H:%M:%S')
        date_text = time.strftime('%d-%m-%Y')
        clock_label.config(text=current_time)
        date_label.config(text=date_text)
        cpu_label.config(text="CPU: " + str(cpu_percent(None)))
        ram_label.config(text="RAM: " + str(virtual_memory().percent))

        if not q.empty():
            warning_window = Toplevel(observer_window)
            # warning_window.attributes("-fullscreen", True)
            warning_window.configure(background='black')
            warning_window.title("Canario")
            warning_window.bind("x", quit)

            warning_label = Label(warning_window, font=('arial', 150, 'bold'), fg='red', bg='black')
            warning_label.pack()
            warning_label.config(text="AVISO")
            detection_message_label = Label(warning_window, font=('arial', 25, 'bold'), fg='white', bg='black', pady=25)
            detection_message_label.pack()
            detection_message_label.config(text="El dispositivo ha detectado posibles amenazas a las " + current_time)
            threat_list = Listbox(warning_window, font='arial', width=100)
            threat_list.pack()
            communication_cut_label = Label(warning_window, font=('arial', 10, 'bold'), fg='white', bg='black', pady=25)
            communication_cut_label.pack()
            communication_cut_label.config(text="Los puertos han sido cerrados para impedir el ataque.")
            index = 0

            while not q.empty():
                threat_list.insert(index, q.get())

        clock_label.after(200, tick)

    tick()
    observer_window.mainloop()

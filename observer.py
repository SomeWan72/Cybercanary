import os
import time
from psutil import cpu_percent, virtual_memory
from tkinter import *


def reset_canary(comm_cut_queue):
    comm_cut_queue.put("Cortar")
    os.execl(sys.executable, sys.executable, *sys.argv)


def observer(detection_queue, comm_cut_queue):
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
    ccc_var = IntVar()
    com_cut_check = Checkbutton(observer_window, font=('arial', 15), fg='white', bg='black', selectcolor='black',
                                text='Cortar las comunicaciones tras un ataque.',
                                variable=ccc_var, onvalue=1, offvalue=0)
    com_cut_check.pack()
    com_cut_check.place(rely=0.975, relx=0.01, anchor=SW)
    com_cut_check.select()
    reset_button = Button(observer_window, font=('arial', 15), text='Reiniciar',
                          command=lambda: reset_canary(comm_cut_queue))
    reset_button.pack()
    reset_button.place(rely=0.975, relx=0.99, anchor=SE)

    def tick():
        current_time = time.strftime('%H:%M:%S')
        date_text = time.strftime('%d-%m-%Y')
        clock_label.config(text=current_time)
        date_label.config(text=date_text)
        cpu_label.config(text="CPU: " + str(cpu_percent(None)))
        ram_label.config(text="RAM: " + str(virtual_memory().percent))

        if not detection_queue.empty():
            com_cut_text = ""
            if ccc_var.get() == 1:
                comm_cut_queue.put("Cortar")
                com_cut_text = "Los puertos han sido cerrados para impedir el ataque."

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
            communication_cut_label.config(text=com_cut_text)
            index = 0

            while not detection_queue.empty():
                threat_list.insert(index, detection_queue.get())

        clock_label.after(200, tick)

    tick()
    observer_window.mainloop()

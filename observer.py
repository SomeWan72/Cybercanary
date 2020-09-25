import os
import subprocess
import time
import socket
from psutil import cpu_percent, virtual_memory
from tkinter import *
from IPy import IP


def error_message(parent_window, msg):
    error_window = Toplevel(parent_window)
    error_window.configure(background='black')
    error_window.title("Error")

    error_label = Label(error_window, font=('arial', 25, 'bold'), fg='red', bg='black')
    error_label.pack()
    error_label.config(text=msg)
    error_button = Button(error_window, text="Aceptar", command=error_window.destroy)
    error_button.pack()


def reset_canary(comm_cut_queue, reset_iptables_queue):
    if not reset_iptables_queue.empty():
        subprocess.run("iptables -D INPUT -j DROP", shell=True)
    comm_cut_queue.put("Cortar")
    time.sleep(1)
    os.execl(sys.executable, sys.executable, *sys.argv)


def delete_ip(observer_window, ip_list, comm_cut_queue, reset_iptables_queue):
    def destroy_ip():
        try:
            bad_ip = str(white_list.get(white_list.curselection()))
            with open("ip.txt", "w") as f:
                for good_ip in ip_list:
                    if str(good_ip).strip("\n") != bad_ip:
                        f.write(str(good_ip) + "\n")
            delete_window.destroy()
            reset_canary(comm_cut_queue, reset_iptables_queue)
        except TclError:
            error_message(delete_window, "Selecciona una IP de la lista")

    delete_window = Toplevel(observer_window)
    delete_window.attributes("-fullscreen", True)
    delete_window.configure(background='black')
    delete_window.title("Canario")

    ip_delete_label = Label(delete_window, font=('arial', 25, 'bold'), fg='skyblue', bg='black')
    ip_delete_label.pack()
    ip_delete_label.config(text="Señale la IP que desea eliminar y, luego, pulse en el botón:")
    ip_delete_label.place(rely=0.1, relx=0.5, anchor=N)

    white_list = Listbox(delete_window, font=('arial', 20), width=50, selectmode=SINGLE)
    white_list.pack()
    white_list.place(rely=0.25, relx=0.5, anchor=N)

    delete_button = Button(delete_window, text="Eliminar", command=destroy_ip)
    delete_button.pack()
    delete_button.place(rely=0.8, relx=0.5, anchor=N)

    back_button = Button(delete_window, text="Regresar", command=delete_window.destroy)
    back_button.pack()
    back_button.place(rely=0.975, relx=0.01, anchor=SW)

    index = 0

    for ip in ip_list:
        white_list.insert(index, ip)
        index += 1


def add_ip(observer_window, ip_list, comm_cut_queue, reset_iptables_queue):
    def insert_ip():
        if ip_entry.get() == "":
            error_message(add_window, "El campo de texto no puede estar vacío")
        else:
            try:
                socket.inet_aton(ip_entry.get())
                if IP(ip_entry.get()) in ip_list:
                    error_message(add_window, "La IP ya está en la lista")
                else:
                    new_ip = str(ip_entry.get())
                    with open("ip.txt", "a") as f:
                        f.write(new_ip + "\n")
                    add_window.destroy()
                    reset_canary(comm_cut_queue, reset_iptables_queue)
            except socket.error:
                error_message(add_window, "La IP debe tener una estructura XXX.XXX.XXX.XXX (p.e. 194.153.205.26)")

    add_window = Toplevel(observer_window)
    add_window.attributes("-fullscreen", True)
    add_window.configure(background='black')
    add_window.title("Canario")

    ip_insert_label = Label(add_window, font=('arial', 25, 'bold'), fg='skyblue', bg='black')
    ip_insert_label.pack()
    ip_insert_label.place(rely=0.1, relx=0.5, anchor=N)
    ip_insert_label.config(text="Inserte la IP para no ser considerada una amenaza:")

    ip_entry = Entry(add_window, font=('arial', 45))
    ip_entry.pack()
    ip_entry.place(rely=0.3, relx=0.5, anchor=N, width=500, height=50)

    add_button = Button(add_window, text="Insertar", command=insert_ip)
    add_button.pack()
    add_button.place(rely=0.5, relx=0.5, anchor=N)

    back_button = Button(add_window, text="Regresar", command=add_window.destroy)
    back_button.pack()
    back_button.place(rely=0.975, relx=0.01, anchor=SW)


def observer(detection_queue, comm_cut_queue, reset_iptables_queue, ip_list):
    observer_window = Tk()
    observer_window.attributes("-fullscreen", True)
    observer_window.configure(background='black')
    observer_window.title("Canario")

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
                          command=lambda: reset_canary(comm_cut_queue, reset_iptables_queue))
    reset_button.pack()
    reset_button.place(rely=0.975, relx=0.99, anchor=SE)

    add_button = Button(observer_window, font=('arial', 15), text='Insertar IP',
                        command=lambda: add_ip(observer_window, ip_list, comm_cut_queue, reset_iptables_queue))
    add_button.pack()
    add_button.place(rely=0.025, relx=0.01, anchor=NW)

    delete_button = Button(observer_window, font=('arial', 15), text='Eliminar IP',
                           command=lambda: delete_ip(observer_window, ip_list, comm_cut_queue, reset_iptables_queue))
    delete_button.pack()
    delete_button.place(rely=0.1, relx=0.01, anchor=NW)

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
                time.sleep(1)
                comm_cut_queue.put("Cortar")
                com_cut_text = "Los puertos han sido cerrados para impedir el ataque."

            warning_window = Toplevel(observer_window)
            warning_window.configure(background='black')
            warning_window.title("Canario")

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
                index += 1

        clock_label.after(200, tick)

    tick()
    observer_window.mainloop()

import tkinter
import psutil
import customtkinter
from PIL import Image,ImageTk
import os
import tkinter as tk
from tkinter import ttk
from tkdial import Dial
import process_list
import sys_info
import matplotlib.pyplot as plt
from scipy.special import jv

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


plt.rcParams["axes.prop_cycle"] = plt.cycler(
    color=["#4C2A85", "#BE96FF", "#957DAD", "#5E366E", "#A98CCC"])

plt.style.use('https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-light.mplstyle')

file_path = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme("green")
root_tk = customtkinter.CTk() 
root_tk.geometry("1225x625")
root_tk.title("Sysbench")
root_tk.configure(expand=False)



# Define the column names for the process list
process_columns = ("PID", "Name", "Username", "CPU", "Memory")




def update_system_info():
    try:
        # Update system information in the GUI
        cpu_percent, memory_percent, network, processes = sys_info.get_system_info()

        # # Update CPU label
        # cpu_label.config(text=f'CPU Usage: {cpu_percent:.2f}%')

        # # Update memory label
        # memory_label.config(text=f'Memory Usage: {memory_percent:.2f}%')

        # # Update network label
        # network_label.config(text=f'Network Usage: Sent: {network.packets_sent} packets, Received: {network.packets_recv} packets')

        # # Update the performance graphs
        #update_performance_graphs(cpu_percent, memory_percent, network.bytes_sent, network.bytes_recv)

        # Update the process list
        update_process_list(processes)
        update_performance_graphs(cpu_percent, memory_percent, network.packets_sent, network.packets_recv)
        # # Update the real-time CPU usage label
        cpu_label.configure(text=f'CPU Usage: {cpu_percent:.2f}%')
        
        dial4.set(cpu_percent)

        # # Update the real-time memory usage label
        # memory_usage_label.configure(text=f'Memory Usage: {memory_percent:.2f}%')

        # # Update the real-time network usage label
        # network_usage_label.config(text=f'Network Usage: Sent: {network.packets_sent} packets, Received: {network.packets_recv} packets')

    except psutil.NoSuchProcess:
        pass

    # Schedule the next update in 1 second
    root_tk.after(1000, update_system_info)

def update_process_list(processes):
    # Clear the process list
    process_list.delete(*process_list.get_children())

    # Populate the process list with the current running processes
    for process in processes:
        process_info = process.as_dict(attrs=['pid', 'name', 'username', 'cpu_percent', 'memory_percent'])
        process_list.insert("", "end", values=(
            process_info['pid'],
            process_info['name'],
            process_info['username'],
            f'{process_info["cpu_percent"]/10:.2f}%',
            f'{process_info["memory_percent"]:.2f}%'
        ))



def update_performance_graphs(cpu_percent, memory_percent, network_sent, network_received):
    # Update CPU graph
    cpu_data.append(cpu_percent)
    if len(cpu_data) > max_data_points:
        cpu_data.pop(0)
    cpu_ax.clear()
    cpu_ax.plot(cpu_data,  label='CPU Usage')
    cpu_ax.fill_between(range(len(cpu_data)), 0, cpu_data)
    cpu_ax.set_ylim(0, 100)
    cpu_ax.set_title('CPU Usage (%)')
    cpu_canvas.draw()










sidebar = customtkinter.CTkFrame(
    master=root_tk,
    width=200,
    height=550,
    corner_radius=10,
    # fg_color="#e8e4e4"
)
sidebar.grid(row=0, column=0, padx=20, pady=20)

def show_tab(tab_id):
    process_frame.pack_forget()
    performance_frame.pack_forget()
    tab_id.tkraise()

image_1=customtkinter.CTkImage(Image.open(file_path+"/assets/performance.png"),size=(26,20))

button_1 = customtkinter.CTkButton(
    master=sidebar,
    text="Performance",
    image=image_1,
    font=("Poppins",14,'bold'),
    command=lambda: show_tab(performance_frame),
    width=175,
    height=32,
    compound="right",
    border_width=0,
    corner_radius=8,
    fg_color="#48a4ec",
    text_color="White",
    border_spacing=8
     # Set the font to Poppins with size 10
)
button_1.place(relx=0.06, rely=0.07)
image_2=customtkinter.CTkImage(Image.open(file_path+"/assets/list.png"),size=(26,20))
button_2 = customtkinter.CTkButton(
    master=sidebar,
    text="Process",
    image=image_2,
    command=lambda: show_tab(process_frame),
    width=175,
    height=32,
    border_width=0, compound="right",
    border_spacing=8,
    corner_radius=8,
    fg_color="#48a4ec",
    text_color="White",
    font=("Poppins",14,'bold') # Set the font to Poppins with size 10
)
button_2.place(relx=0.06, rely=0.16)

right_frame = customtkinter.CTkFrame(
    master=root_tk,
    width=950,
    height=550,
    corner_radius=10,
    fg_color="transparent"
)
right_frame.grid(row=0, column=1, padx=0, pady=20)

process_frame = customtkinter.CTkFrame(
    master=right_frame,
    width=950,
    height=550,
    corner_radius=10,
    # fg_color="#e8e4e4"
)
process_frame.grid(row=0, column=1, padx=0, pady=20)
l2=customtkinter.CTkLabel(master=process_frame, text="Process Chart",font=('Century Gothic',23),fg_color="transparent",bg_color="transparent")
l2.place(x=-10, y=1)
l2.pack()


performance_frame = customtkinter.CTkFrame(
    master=right_frame,
    width=950,
    height=550,
    corner_radius=10,
    # fg_color="#e8e4e4"
)
performance_frame.grid(row=0, column=1, padx=0, pady=20)



tabview= customtkinter.CTkTabview(performance_frame,width=938,height=540,corner_radius=10,border_width=1,fg_color='white')

cpu_tab= tabview.add("CPU")
memory_tab=tabview.add("Memory")
network_tab=tabview.add("Network")


cpu_text_frame=customtkinter.CTkFrame(cpu_tab,fg_color='white')

dial4 = Dial(master=cpu_text_frame, color_gradient=("red", "blue"),
             text_color="white", text="", unit_width=10, radius=110, scroll=False)
dial4.pack(side="left")  # Changing the pack placement to the left side

cpu_label = customtkinter.CTkLabel(cpu_text_frame, font=('Poppins', 27, 'bold'),text_color='#228B22')
cpu_label.pack(side="left", padx=10)  # Placing the label to the left with some padding

cpu_text_frame.pack(anchor="center", pady=5)



cpu_data = []
max_data_points = 120
cpu_fig = plt.Figure(figsize=(8,2.5)) 
cpu_ax = cpu_fig.add_subplot(111)
cpu_canvas = FigureCanvasTkAgg(cpu_fig, master=cpu_tab)
cpu_canvas.get_tk_widget().pack()






tabview.pack()













#process list
process_list=process_list.process_list(process_frame)
process_list.pack(expand=True, fill=tk.BOTH)

# Start updating system information and performance graphs
update_system_info()


root_tk.mainloop()

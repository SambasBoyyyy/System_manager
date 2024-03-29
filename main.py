import tkinter
import platform
import psutil
import customtkinter
# from PIL import Image,ImageTk
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

        # Update the process list
        update_process_list(processes)
        update_performance_graphs(cpu_percent, memory_percent, network.bytes_sent, network.bytes_recv)
        # # Update the real-time CPU usage label
        cpu_label.configure(text=f'CPU Usage: {cpu_percent:.2f}%')
        
        dial4.set(cpu_percent)

        # # Update the real-time memory usage label
        memory_label.configure(text=f'Memory Usage: {memory_percent:.2f}%')
        dial5.set(memory_percent)

        # # Update the real-time network usage label
        network_usage_label.configure(text=f'Network Usage: Sent: {network.bytes_sent} bytes, Received: {network.bytes_recv} bytes')

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
    cpu_ax.plot(cpu_data, label='CPU Usage')
    cpu_ax.fill_between(range(len(cpu_data)), 0, cpu_data)
    cpu_ax.set_ylim(0, 100)
    cpu_ax.set_title('CPU Usage (%)')
    cpu_canvas.draw()
    # Update Memory graph
    memory_data.append(memory_percent)
    if len(memory_data) > max_data_points:
        memory_data.pop(0)
    memory_ax.clear()
    memory_ax.plot(memory_data ,label='Memory Usage',color='blue')
    memory_ax.fill_between(range(len(memory_data)), 0, memory_data)
    memory_ax.set_ylim(0, 100)
    memory_ax.set_title('Memory Usage (%)')
    memory_canvas.draw()
 # Update Network graph
    network_sent_data.append(network_sent)
    network_received_data.append(network_received)
    if len(network_sent_data) > max_data_points:
        network_sent_data.pop(0)
        network_received_data.pop(0)
    network_ax.clear()
    network_ax.plot(network_sent_data, color='blue', label='Sent')
    network_ax.plot(network_received_data, color='purple', label='Received')
    network_ax.set_title('Network Usage (Packets)')
    network_ax.legend()
    network_canvas.draw()
    









sidebar = customtkinter.CTkFrame(
    master=root_tk,
    width=200,
    height=550,
    corner_radius=10,
    # fg_color="#e8e4e4"
)
sidebar.grid(row=0, column=0, padx=20, pady=20)

def show_tab(tab_id):
     # A list of frames to manage
    # A list of frames to manage
    frames = [specs_frame, performance_frame, process_frame]

    # Hide all frames placed using pack
    for frame in frames:
        frame.pack_forget()

    # Hide all frames placed using grid
    for frame in frames:
        frame.grid_remove()

    # Show the selected frame
    tab_id.pack()  # For frames placed using pack
    tab_id.grid()

button_0 = customtkinter.CTkButton(
    master=sidebar,
    text="Specs",
    command=lambda: show_tab(specs_frame),
    width=175,
    height=32,
    border_width=0, compound="right",
    border_spacing=8,
    corner_radius=8,
    fg_color="#48a4ec",
    text_color="White",
    font=("Poppins",14,'bold') # Set the font to Poppins with size 10
)
button_0.place(relx=0.06, rely=0.07)

button_1 = customtkinter.CTkButton(
    master=sidebar,
    text="Performance",
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
button_1.place(relx=0.06, rely=0.25)
button_2 = customtkinter.CTkButton(
    master=sidebar,
    text="Process",
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
button_2.place(relx=0.06, rely=0.34)



right_frame = customtkinter.CTkFrame(
    master=root_tk,
    width=950,
    height=550,
    corner_radius=10,
    fg_color="transparent"
)
right_frame.grid(row=0, column=1, padx=0, pady=20)
def get_spec_info():
    spec_frame_info = {
        "Computer network name": platform.node(),
        "Machine type": platform.machine(),
        "Processor type": platform.processor(),
        "Platform type": platform.platform(),
        "Operating system": platform.system(),
        "Operating system release": platform.release(),
        "Operating system version": platform.version(),
        "Number of physical cores": psutil.cpu_count(logical=False),
        "Number of logical cores": psutil.cpu_count(logical=True),
        "Min CPU frequency": f"{psutil.cpu_freq().min} Mhz",
        "Max CPU frequency": f"{psutil.cpu_freq().max} Mhz",
        "Total RAM installed": f"{round(psutil.virtual_memory().total / 1e+9, 2)} GB",
        "Current directory": os.getcwd(),
        "Current Disk": f"{psutil.disk_usage(os.getcwd()).total / 1e+9:.2f} GB"
    }
    return spec_frame_info

def update_spec_info():
    spec_info = get_spec_info()
    formatted_info = "\n".join([f"{key}: {value}" for key, value in spec_info.items()])

    # Update the text label in the specs frame
    specs_text.configure(text=formatted_info)
    
specs_frame = customtkinter.CTkFrame(
    master=right_frame,
    width=950,
    height=550,
    corner_radius=10,
    fg_color="white"
)
specs_frame.grid(row=0, column=1, padx=0, pady=20)
specs_text_frame=customtkinter.CTkFrame(specs_frame,fg_color='white')
specs_text=customtkinter.CTkLabel(specs_text_frame,font=('Poppins', 22, 'bold'),)
                                  

specs_text_frame.pack()
specs_text.pack(padx=120,pady=95)






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


#memry tab
memory_text_frame=customtkinter.CTkFrame(memory_tab,fg_color='white')
dial5 = Dial(master=memory_text_frame, color_gradient=( "blue","red"),
             text_color="white", text="", unit_width=10, radius=110, scroll=False)
dial5.pack(side="left")
memory_label = customtkinter.CTkLabel(memory_text_frame, font=('Poppins', 27, 'bold'),text_color='#228B22')
memory_label.pack(side="left", padx=10)
memory_text_frame.pack(anchor="center", pady=5)

memory_data = []
max_data_points = 120
memory_fig = plt.Figure(figsize=(8, 2.5))
memory_ax = memory_fig.add_subplot(111)
memory_canvas = FigureCanvasTkAgg(memory_fig, master=memory_tab)
memory_canvas.get_tk_widget().pack()


network_sent_data = []
network_received_data = []
network_fig = plt.Figure(figsize=(8, 3.5))
network_ax = network_fig.add_subplot(111)
network_canvas = FigureCanvasTkAgg(network_fig, master=network_tab)
network_canvas.get_tk_widget().pack()
network_usage_label = customtkinter.CTkLabel(network_tab,font=('Poppins', 27, 'bold'))
network_usage_label.pack()

tabview.pack()













#process list
process_list=process_list.process_list(process_frame)
process_list.pack(expand=True, fill=tk.BOTH)

# Start updating system information and performance graphs
update_system_info()
update_spec_info()


root_tk.mainloop()

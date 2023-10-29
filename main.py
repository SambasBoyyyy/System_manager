import tkinter
import psutil
import customtkinter
from PIL import Image,ImageTk
import os
import tkinter as tk
from tkinter import ttk


file_path = os.path.dirname(os.path.realpath(__file__))
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("green")
root_tk = customtkinter.CTk() 
root_tk.geometry("1225x625")
root_tk.title("Sysbench")



# Define the column names for the process list
process_columns = ("PID", "Name", "Username", "CPU", "Memory")
def get_system_info():
    # Retrieve system information using psutil library
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    network = psutil.net_io_counters()
    processes = list(psutil.process_iter())

    # Sort the processes by CPU usage in descending order
    processes.sort(key=lambda x: x.cpu_percent(), reverse=True)

    return cpu_percent, memory.percent, network, processes



def update_system_info():
    try:
        # Update system information in the GUI
        cpu_percent, memory_percent, network, processes = get_system_info()

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

        # # Update the real-time CPU usage label
        cpu_label.configure(text=f'CPU Usage: {cpu_percent:.2f}%')

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



tabview= customtkinter.CTkTabview(performance_frame,width=938,height=540,corner_radius=10,border_width=1)

cpu_tab= tabview.add("CPU")
memory_tab=tabview.add("Memory")
network_tab=tabview.add("Network")
# cpu_tab.grid_columnconfigure(0,weight=1)
# memory_tab.grid_columnconfigure(0,weight=1)
# network_tab.grid_columnconfigure(0,weight=1)


cpu_text_frame=customtkinter.CTkFrame(cpu_tab,width=100,height=250)
cpu_text_frame.pack(anchor="w",padx=20, pady=30)
cpu_text_frame.pack()
# # cpu_text=ttk.Label(cpu_text_frame,text="CPU Usage :")
# # cpu_text.pack()

cpu_label = customtkinter.CTkLabel(cpu_text_frame,font=('Poppins', 27,'bold'),justify="right")
cpu_label.pack(anchor="w",padx=125, pady=30)
tabview.pack()




# Create a tab for the process list
process_list = ttk.Treeview(process_frame, columns=process_columns, show="headings")


for col in process_columns:
    process_list.heading(col, text=col)
    process_list.column(col,width=183)
    
# Create a vertical scrollbar
process_scrollbar = ttk.Scrollbar(process_frame, orient=tk.VERTICAL, command=process_list.yview)
process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the Treeview widget to use the scrollbar
process_list.configure(yscrollcommand=process_scrollbar.set,height=23)
process_list.pack(expand=True, fill=tk.BOTH)

# Start updating system information and performance graphs
update_system_info()


root_tk.mainloop()

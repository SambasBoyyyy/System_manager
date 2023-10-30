import tkinter as tk
from tkinter import ttk

def process_list(frame):
    # Create a tab for the process list
    process_columns = ("PID", "Name", "Username", "CPU", "Memory")
    process_list = ttk.Treeview(frame, columns=process_columns, show="headings")

    for col in process_columns:
        process_list.heading(col, text=col)
        process_list.column(col, width=183)
    
    # Create a vertical scrollbar
    process_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=process_list.yview)
    process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the Treeview widget to use the scrollbar
    process_list.configure(yscrollcommand=process_scrollbar.set, height=24)

    return process_list

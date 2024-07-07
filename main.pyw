from pywinauto import Desktop
import time
import tkinter as tk
from pystray import MenuItem as item
from pystray import Icon
from PIL import Image, ImageTk

import os
import threading
import random


distractions = []
# Function to handle button click
def add_to_list():
    input_text = entry.get()
    if input_text:
        distractions.append(input_text)
        listbox.insert(tk.END, input_text)
        entry.delete(0, tk.END)
    
def filter(dec_windows: list) -> list:
    filt_windows = []
    for window in dec_windows:
        if window=='':
            continue
        filt_windows.append(window[window.rfind('-')+1:].strip())
    return filt_windows

def search_keyword(dec_windows: list, keyword: str) -> bool:
    for window in dec_windows:
        if keyword.lower() in window.lower():
            return True
    return False

root = tk.Tk()

this_path = os.path.dirname(os.path.abspath(__file__))
path_to_image = os.path.join(this_path, 'quiet-icon.png')
ICON = Image.open(path_to_image)

root.iconphoto(True, ImageTk.PhotoImage(ICON))
root.title("No Distractions.")
root.geometry("300x350")

tk.Label(text="Looks like you want to stay focused. Good.").pack()
tk.Label(text="What's distracting you? Please list them.").pack()

closed = False

def quit_window(icon, item):
    icon.stop()
    root.quit()
    global closed
    closed = True

def show_window(icon, item):
    icon.stop()
    root.deiconify()
    
def hide_gui():
    # Put window in system tray
    root.withdraw()
    menu = (item('Quit', quit_window), item('Show', show_window))
    icon = Icon("name", ICON, "Tray Icon", menu)
    
    icon.run_detached()

def open_new_window(distraction: str):
    new = tk.Toplevel(root)
    
    # To make windowed fullscreen (commented out):
    # new.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
    
    root.update_idletasks()
    
    # Have window be created at random location (harder to close)
    rand_width  = random.randint(0, root.winfo_screenwidth()-500)
    rand_height = random.randint(0, root.winfo_screenheight()-500)
    new.geometry(f"500x500+{rand_width}+{rand_height}")
    new.title("Close it.")
    
    #Create a Label in New window
    tk.Label(new, text="Close "+distraction, font=('Helvetica 17 bold'), ).pack(pady=30)
    new.attributes('-topmost', True)

def get_windows_open() -> list:
    windows = Desktop(backend="uia").windows()
    dec_windows = [w.window_text() for w in windows]
    
    return dec_windows
def done_adding():
    while closed==False:
        for distraction in distractions:
            if search_keyword(get_windows_open(), distraction):
                root.after(0, open_new_window(distraction))
                time.sleep(10)
                if search_keyword(get_windows_open(), distraction)==False:
                    continue
                
                for _ in range(3):
                    root.after(0, open_new_window(distraction))
                    time.sleep(1)
                time.sleep(15)
                if search_keyword(get_windows_open(), distraction)==False:
                    continue
                
                for _ in range(5):
                    root.after(0, open_new_window(distraction))
                    time.sleep(0.6)
                time.sleep(30)
                if search_keyword(get_windows_open(), distraction)==False:
                    continue
                
                for _ in range(30):
                    root.after(0, open_new_window(distraction))
                    time.sleep(0.5)
                time.sleep(45)
                
        
        time.sleep(1.5)

entry = tk.Entry(root, width=30)
entry.pack(padx=10, pady=10)

add_button = tk.Button(root, text="Add to List", command=add_to_list)
add_button.pack(padx=10, pady=10)

listbox = tk.Listbox(root, width=30, height=10)
listbox.pack(padx=10, pady=10)

done_button = tk.Button(root, text="Done", command=hide_gui)
done_button.pack(padx=10, pady=10)

# Start side thread of application
thread = threading.Thread(target=done_adding, daemon=True)
thread.start()
    
root.mainloop()
    



from tkinter import ttk, messagebox, filedialog
from tkinter import *
from pytube import YouTube
from threading import *
import os

res = ""
type = ""
fps = ""


def threading1():
    t = Thread(target=get_link)
    t.start()


def get_link():
    try:
        link = YouTube(name_var.get())
        link_list = []
        global res, type, fps
        stream.set("--Select--")
        stream['values'] = ""
        info['text'] = "Information:\n\n\n"

        wait['text'] = "Getting stream data... Wait for a moment."
        for i in range(len(link.streams)):
            res = link.streams[i].resolution
            type = link.streams[i].mime_type
            if link.streams[i].resolution is not None:
                fps = link.streams[i].fps
            else:
                fps = None
            link_list.append(f"Resolution: {res}, Type: {type}, FPS: {fps}")

        wait['text'] = "Now select Stream from below:"
        stream['values'] = link_list
    except:
        wait['text'] = "Enter valid Youtube Video Link"
        messagebox.showerror("Invalid Link", "Enter Valid YouTube Video Link")


root = Tk()
root.title("YouTube Video Downloader")
root.geometry("600x560")
root.resizable(0, 0)
root.configure(bg="LightGrey")
root.wm_iconbitmap('icon.ico')

Label(root, text="YouTube Video Downloader", fg="Black", bg="LightGrey", font="times 25 bold", pady='10').pack()

Frame(root, bg="White").pack(fill=X, pady=10)

Label(root, text="Enter link of YouTube video", bg="LightGrey", font="arial 15 bold", pady='5').pack(padx='5')

name_var = StringVar()

entry = Entry(root, textvariable=name_var, font="Calibri 15")
entry.pack(padx='10', fill='x')

submit = Button(root, text="Click Here", command=threading1, padx=5, pady=5)
submit.pack(pady="10")

wait = Label(root, text="---------------- ", bg="LightGrey", font="arial 10 bold")
wait.pack()


def threading2(event):
    t = Thread(target=show_info)
    t.start()


def show_info():
    info['text'] = "Information:\nFetching Data...\n\n"
    link = YouTube(name_var.get())
    info['text'] = f"Information:\nName: {link.title}\nQuality: {link.streams[stream.current()].resolution}, " \
                   f"{link.streams[stream.current()].type} " \
                   f"\nSize: {link.streams[stream.current()].filesize / (1024 * 1024):.3f} MB"


Label(root, text="Select Stream", bg="LightGrey", font="arial 10 bold").pack(anchor="w", padx='5', pady='5')
stream = ttk.Combobox(root, state="readonly")
stream.pack(fill='x', padx='10')
stream.set("--Select--")

stream.bind("<<ComboboxSelected>>", threading2)

info = Label(root, text="Information: \n\n\n", font="arial 10 bold", bg="LightGrey", justify="left")
info.pack(anchor="w", padx='10', pady='10')

directory = StringVar()
Label(root, text="Enter Path to Download", font="arial 10 bold", bg="LightGrey").pack(anchor="w", padx='10', pady='5')

label = Label(root, bg="LightGrey")
label.pack(fill='x', padx='10')
path = Entry(label, textvariable=directory, font="Calibri 12", width='61')
path.grid()


def browse():
    download_dir = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH", title="Save Video")
    directory.set(download_dir)
    path['text'] = directory


browse = Button(label, text="Browse", command=browse, width="9")
browse.grid(row=0, column=1, padx='10')


def threading3():
    t = Thread(target=click_download)
    t.start()


def click_download():
    if name_var.get() == "":
        messagebox.showerror("Error", "Enter YouTube Video Link.")
    elif stream.get() == "--Select--":
        messagebox.showerror("Stream Error", "Select stream.")
    elif os.path.exists(directory.get()):
        status['text'] = "Download Status: Downloading..."
        link = YouTube(name_var.get())
        link.streams[stream.current()].download(directory.get())
        status['text'] = "Download Status: Download Complete"
    else:
        messagebox.showerror("Invalid Path", "Enter valid path.")


download = Button(root, text="Download", padx=5, pady=5, command=threading3)
download.pack(pady='10')

status = Label(root, text="Download Status:", font="arial 10 bold", bg="LightGrey", justify="left")
status.pack(anchor="w", padx='10', pady='10')

root.mainloop()

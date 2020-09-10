from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from pytube import YouTube
from threading import Thread
import pytube
import urllib
import time

directoryPath = r"C:\Users\Admin\Downloads"  # TODO: Default path
availableStreams = []
link = ""
title = ""
download_button = ""
youtube_link_value = ""
youtube_link_error = ""
downloading_status = ""
directory_status = ""
available_streams_in_youtube = ""
total_file_size = 0  # TODO:Selected file size in bytes


def select_directory():
    global directoryPath, link
    directoryPath = filedialog.askdirectory()
    directory_status.config(text=directoryPath, fg="green")


def download_file():
    global total_file_size, availableStreams
    downloading_status.config(text="Downloading Starting...", fg="green")
    stream = available_streams_in_youtube.get()
    if stream:  # TODO:user select any stream
        stream = stream.split(" ")
        file_type = stream[0]
        choice = stream[1]
        if file_type == "Video":
            yt = YouTube(link)
            video = yt.streams.filter(res=choice, progressive=True).first()
            video.download(directoryPath)
            total_file_size = video.filesize
        else:
            yt = YouTube(link)
            audio = yt.streams.filter(abr=choice, progressive=False).first()
            audio.download(directoryPath)
            total_file_size = audio.filesize
    else:  # TODO: Default download
        yt = YouTube(link)
        video = yt.streams.first()
        video.download(directoryPath)
        total_file_size = video.filesize
    downloading_status.config(text="Download Completed !!!")
    availableStreams = []


def call_back(var, index, mode):
    global link
    youtube_link_error.config(text="Waiting for Data Fetch", fg="green")
    link = youtube_link_value.get()
    time.sleep(2)
    try:
        yt = YouTube(link)
        final_title = yt.title
        title.config(text=final_title)
        videos = yt.streams.filter(res="1080p", progressive=True)
        if videos:
            availableStreams.append("Video 1080p")
        videos = yt.streams.filter(res="720p", progressive=True)
        if videos:
            availableStreams.append("Video 720p")
        videos = yt.streams.filter(res="480p", progressive=True)
        if videos:
            availableStreams.append("Video 480p")
        videos = yt.streams.filter(res="360p", progressive=True)
        if videos:
            availableStreams.append("Video 360p")
        videos = yt.streams.filter(res="240p", progressive=True)
        if videos:
            availableStreams.append("Video 240p")
        videos = yt.streams.filter(res="144p", progressive=True)
        if videos:
            availableStreams.append("Video 144p")
        videos = yt.streams.filter(abr="160kbps", progressive=False)
        if videos:
            availableStreams.append("Audio 160kbps")
        videos = yt.streams.filter(abr="128kbps", progressive=False)
        if videos:
            availableStreams.append("Audio 128kbps")
        available_streams_in_youtube.config(value=availableStreams)
        youtube_link_error.config(text="", fg="green")
        download_button["state"] = NORMAL
        download_button["bg"] = "yellow"
    except pytube.exceptions.RegexMatchError as e:
        youtube_link_error.config(text="Invalid Link !!!", fg="red")
    except urllib.error.URLError as e:
        youtube_link_error.config(text="Check Your Network Connection", fg="red")


class OwnThreadFirst(Thread):
    def run(self):
        # TODO: Display
        youtube_link = Label(root, text="Paste YouTube Link Here :-", fg="#5FB0E4", bg="#2B2B2B", font=("", 20), pady=10)
        youtube_link.pack()

        global youtube_link_value, youtube_link_error, \
            available_streams_in_youtube, title, directory_status, downloading_status, download_button
        youtube_link_value = StringVar()
        # TODO: here call second thread(t2)
        t2.start()
        Entry(root, textvariable=youtube_link_value, width=50, bg="#3C3F41", fg="green").pack()

        youtube_link_error = Label(root, text="", fg="red", bg="#2B2B2B", font=("", 15), pady=5)
        youtube_link_error.pack()

        directory = Label(root, text="Where to Download File :-", fg="#5FB0E4", bg="#2B2B2B", font=("", 15), pady=10)
        directory.pack()

        directory_button = Button(root, text="Choose Directory", command=select_directory, bg="yellow", fg="black")
        directory_button.pack()

        directory_status = Label(root, text=r"Default Directory:- C:\Users\Admin\Downloads",
                                 bg="#2B2B2B", fg="green", font=("", 15))
        directory_status.pack()

        file_choose = Label(root, text="Select File Type :-", fg="#5FB0E4", bg="#2B2B2B", font=("", 15), pady=5)
        file_choose.pack()

        available_streams_in_youtube = ttk.Combobox(root, values=availableStreams)
        available_streams_in_youtube.pack()

        download_button = Button(root, text="Download", state="disabled", activebackground="pink",
                                 width=15, bg="yellow", command=download_file)
        download_button.pack(pady=10)

        # progressbar = ttk.Progressbar(root, orient="horizontal", length=400, mode='determinate')
        # progressbar.pack(pady=10)

        downloading_status = Label(root, text="", bg="#2B2B2B", fg="green", font=("", 15))
        downloading_status.pack()

        title = Label(root, text="", bg="#2B2B2B", fg="#5FB0E4", font=("", 8))
        title.pack()

        developer_status = Label(root, text="Developed By RKNANDA", bg="#2B2B2B", fg="red", font=("arial", 20, "bold"))
        developer_status.pack(pady=15)


class OwnThreadSecond(Thread):
    def run(self):
        youtube_link_value.trace_add('write', call_back)


t1 = OwnThreadFirst()
t2 = OwnThreadSecond()

# TODO:Let's Start GUI Application from here
root = Tk()

# TODO:Geometry
root.geometry("550x480")   # "width x height"
root.minsize(550, 480)     # width , height
root.maxsize(550, 480)     # width , height

# TODO:title
root.title("YouTube Downloader")
root['bg'] = "#2B2B2B"

# TODO:icon
root.wm_iconbitmap('iconYT.ico')

# TODO:start t1 Thread
t1.start()

# TODO: Tkinter Loop
root.mainloop()




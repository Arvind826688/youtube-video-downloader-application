from pytube import Playlist, YouTube
import os
from tkinter import Tk, Label, Entry, Button, filedialog, messagebox
import re

def sanitize_filename(filename):
    """Sanitize the filename to be valid across different operating systems."""
    return re.sub(r'[\\/*?:"<>|]', "", filename)

def download_youtube_video(youtube_url, save_path):
    try:
        yt = YouTube(youtube_url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
        if stream is None:
            raise Exception("No progressive stream available")
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        stream.download(save_path)
        messagebox.showinfo("Success", f"Downloaded: {yt.title} successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def download_youtube_playlist(playlist_url, save_path):
    try:
        playlist = Playlist(playlist_url)
        playlist_folder = os.path.join(save_path, sanitize_filename(playlist.title))
        if not os.path.exists(playlist_folder):
            os.makedirs(playlist_folder)
        for video in playlist.videos:
            video_title = sanitize_filename(video.title)
            video_filename = f"{video_title}.mp4"
            video_filepath = os.path.join(playlist_folder, video_filename)
            if os.path.isfile(video_filepath):
                print(f"Already downloaded: {video_title}")
                continue
            try:
                stream = video.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
                if stream is None:
                    raise Exception("No progressive stream available")
                stream.download(output_path=playlist_folder, filename=video_filename)
                print(f"Downloaded: {video_title}")
            except Exception as e:
                print(f"Failed to download {video_title}: {e}")
        messagebox.showinfo("Success", "Playlist downloaded successfully")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def select_save_path():
    path = filedialog.askdirectory()
    if path:
        save_path_entry.delete(0, 'end')
        save_path_entry.insert(0, path)

def on_download_video():
    youtube_url = url_entry.get()
    save_path = save_path_entry.get()
    if youtube_url and save_path:
        download_youtube_video(youtube_url, save_path)
    else:
        messagebox.showerror("Error", "Please enter both URL and Save Path")

def on_download_playlist():
    playlist_url = url_entry.get()
    save_path = save_path_entry.get()
    if playlist_url and save_path:
        download_youtube_playlist(playlist_url, save_path)
    else:
        messagebox.showerror("Error", "Please enter both URL and Save Path")

# Initialize the main window
root = Tk()
root.title("YouTube Downloader")

# Create and place labels, entries, and buttons
Label(root, text="YouTube Video/Playlist URL:").grid(row=0, column=0, padx=10, pady=10)
url_entry = Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Save Path:").grid(row=1, column=0, padx=10, pady=10)
save_path_entry = Entry(root, width=50)
save_path_entry.grid(row=1, column=1, padx=10, pady=10)

Button(root, text="Browse", command=select_save_path).grid(row=1, column=2, padx=10, pady=10)
Button(root, text="Download Video", command=on_download_video).grid(row=2, column=0, padx=10, pady=10)
Button(root, text="Download Playlist", command=on_download_playlist).grid(row=2, column=1, padx=10, pady=10)

# Start the main loop
root.mainloop()

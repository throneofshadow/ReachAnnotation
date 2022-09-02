""" GUI for use with ReachMaster/ReachProcess data, code repurposed from https://github.com/PaulleDemon/tkVideoPlayer
    Code below written by Nicholas Chin, Brett Nelson. MIT LICENSE
    """
import datetime
import tkinter as tk
from tkinter import filedialog
from reachannotation_gui import ReachAnnotation


def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())


def load_video():
    """ loads the video """
    file_path = filedialog.askopenfilename()

    if file_path:
        vid_player.load(file_path)

        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)


def seek(value):
    """ used to seek a specific timeframe """
    vid_player.seek(int(value))


def skip(value: int):
    """ skip seconds """
    vid_player.seek(int(progress_slider.get())+value)
    progress_value.set(progress_slider.get() + value)


def play_pause():
    """ pauses and plays """
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"

    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"


def video_ended(event):
    """ handle video ended """
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)


root = tk.Tk()
root.title("Tkinter media")

load_btn = tk.Button(root, text="Load", command=load_video)
load_btn.pack()

# define video player
vid_player = ReachAnnotation(scaled=True, master=root)
vid_player.pack(expand=True, fill="both")

# Add button for playing/pausing video
play_pause_btn = tk.Button(root, text="Play", command=play_pause)
play_pause_btn.pack()

# Add button for skipping +- 5 frame intervals
skip_plus_5sec = tk.Button(root, text="Skip -5 sec", command=lambda: skip(-5))
skip_plus_5sec.pack(side="left")

# add button for time
start_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

# add slider value to indicate where exactly we are at in video.
progress_value = tk.IntVar(root)
progress_slider = tk.Scale(root, variable=progress_value, from_=0, to=0, orient="horizontal", command=seek)
# progress_slider.bind("<ButtonRelease-1>", seek)
progress_slider.pack(side="left", fill="x", expand=True)
# Display end times at end of slider.
end_time = tk.Label(root, text=str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")

vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)
vid_player.bind("<<Ended>>", video_ended)

skip_plus_5sec = tk.Button(root, text="Skip +5 sec", command=lambda: skip(5))
skip_plus_5sec.pack(side="left")

# add method for obtaining .txt file paths for start/stop times, classification

# add method for displaying both outputs in right side

# add method for editing ouputs in right side

# add method for saving outputs in right side

# add method for selecting behavior w/ mouse input

# add method for selection to "seek" frame selected


root.mainloop()

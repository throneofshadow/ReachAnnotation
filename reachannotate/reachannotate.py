""" GUI for use with ReachMaster/ReachProcess data, code repurposed from https://github.com/PaulleDemon/tkVideoPlayer
    Code below written by Nicholas Chin, Brett Nelson. MIT LICENSE
    """
import datetime
import pdb
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import glob
import pandas as pd
from reachannotation_gui import ReachAnnotation


def update_duration(event):
    """ updates the duration after finding the duration """
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration


def update_scale(event):
    """ updates the scale value """
    progress_value.set(vid_player.current_duration())


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


def selectItem(a):
    curItem = tree.focus()  # current row selection in tree
    trial_time = int(float(tree.item(curItem)['values'][1]))  # gets first value from dictionary of row values
    seek_trial_value(trial_time)  # seeks to start frame in behavior.


def seek_trial_value(trial_val):
    seek(trial_val)


def editItem():
    curItem = tree.focus() # finds trial row
    for index, items in enumerate(tree.item(curItem)['values']):  # iterate over list of values
        if index < 2:
            pass
        else:  # this is where we need help
            # Input new, NA
            if index == 2:
                x = input('Please enter new value for Trial Type (0 for no reach, 1 for Reach)')
                tree.set(curItem, '#3', str(x))
                #tree.item(curItem)[index] = str(x)
            if index == 3:
                x = input('Please enter new value for number of reaches')
                tree.item(curItem)[index] = str(x)
            if index == 4:
                x = input('Please enter new value for reach start time(s)')
                tree.item(curItem)[index] = str(x)
            if index == 5:
                x = input('Please enter new value for reach stop time(s)')
                tree.item(curItem)[index] = str(x)
            if index == 6:
                x = input('Please enter new value for handedness of reach')
                tree.item(curItem)[index] = str(x)
            if index == 7:
                x = input('Please enter new value for tug of war (0 none in trial)')
                tree.item(curItem)[index] = str(x)
    VL.edit_csv_file(curItem)
    return


def pack_tree_with_csv(csv_data):
    for index, data in csv_data.iterrows():
        tree.insert('', 'end', text='1', values=(str(data[0]), str(data[1]), str(data[2]),
                                                 str(data[3]), str(data[4]), str(data[5]), str(data[6]),
                                                 str(data[7])))
    tree.pack(side='left')


def load_video():
    file_path = filedialog.askopenfilename()
    vid_player.load(file_path)
    progress_slider.config(to=0, from_=0)
    play_pause_btn["text"] = "Play"
    progress_value.set(0)

class VideoLoader:

    def __init__(self):
        self.video_address = None
        self.file_path = None
        self.csv_address = 'trial_times.csv'
        self.csv_data = None

    def load_video(self, windows=False):
        """ loads the video """
        if windows:
            file_ids = str.rsplit(file_path, '//')
        else:
            file_ids = str.rsplit(file_path,'/')
        file_n = file_ids[0:-1]
        for i, f in enumerate(file_n):
            if i == 0:
                self.file_path = f
            else:
                self.file_path += '/'
                self.file_path += f
        # search for a .csv file inside of directory, automatic load
        self.csv_address = self.file_path + '/trial_times.csv'
        self.csv_data = pd.read_csv(self.csv_address)
        pack_tree_with_csv(self.csv_data)
        # for
        if file_path:
            load_video(file_path)

    def edit_csv_file(self, curItem):
        """ Function to edit and save edits in populated csv file. """
        values = tree.item(curItem)['values']
        index = values[0]  # index of dataframe to save
        if self.csv_data:
            self.csv_data[index, :] = values
        else:
            self.csv_data = pd.read_csv(self.csv_address)
            self.csv_data[index, :] = values
        self.csv_data.to_csv(self.csv_address,index=False)
        return


VL = VideoLoader()

root = tk.Tk()
root.title("Tkinter media")

tree = ttk.Treeview(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=5)

tree.column("# 1", anchor=CENTER,  width=70)
tree.heading("# 1", text="Trial Number")
tree.column("# 2", anchor=CENTER,  width=70)
tree.heading("# 2", text="Start Time")
tree.column("# 3", anchor=CENTER, stretch=NO, width=70)
tree.heading("# 3", text="Trial?")
tree.column("# 4", anchor=CENTER, stretch=NO, width=70)
tree.heading("# 4", text="Num Reaches")
tree.column("# 5", anchor=CENTER, stretch=NO, width=70)
tree.heading("# 5", text="Reaching Start Times")
tree.column("# 6", anchor=CENTER, stretch=NO, width=70)
tree.heading("# 6", text="Reaching Stop Times")
tree.column("# 7", anchor=CENTER, stretch=NO, width=70)
tree.heading("# 7 ", text="Handedness")
tree.column("# 8", anchor=CENTER, stretch=NO, width=70)
tree.heading("# 8", text="Tug of War")

# Vertical scrollbar for tree
treeScroll = ttk.Scrollbar(root)
treeScroll.configure(command=tree.yview)
tree.configure(yscrollcommand=treeScroll.set)
treeScroll.pack(side=RIGHT, fill=BOTH)
tree.pack()
# add method for editing ouputs in right side


tree.bind('<ButtonRelease-1>', selectItem)
tree.bind('<ButtonRelease-2>', editItem)

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

#Load Video Button
load_btn = tk.Button(root, text="Load", command=load_video)
load_btn.pack(side='left')

update_button = tk.Button(root, text="Update Record", command=editItem)
update_button.pack()

# define video player


# add method for saving outputs in right side

# add method for selecting behavior w/ mouse input


root.mainloop()
""" GUI for use with ReachMaster/ReachProcess data, code repurposed from https://github.com/PaulleDemon/tkVideoPlayer
    Code below written by Nicholas Chin, Brett Nelson. MIT LICENSE
    """
import datetime
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import ttk
import pandas as pd
from reachannotate.reachannotation_gui import ReachAnnotation


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
    vid_player.seek(int(progress_slider.get()) + value)
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


class TEdit(ttk.Treeview):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.bind("<Double-1>", self.selectItem2)

    def selectItem2(self, event):
        # Identifies the location of the click
        region_clicked = self.identify_region(event.x, event.y)

        # Focus find column
        column = self.identify_column(event.x)
        # Stratify for column index to find index of selection focus
        column_index = int(column[1:]) - 1

        # Focus and find selected cell
        selected_id = self.focus()
        selected_values = self.item(selected_id)
        if column == "#0":
            selected_text = selected_values.get("text")
        else:
            selected_text = selected_values.get("values")[column_index]

        # Cell binding box -- find width and size of the box
        column_box = self.bbox(selected_id, column)

        # Cell binding box -- double click event
        entry_edit = ttk.Entry(root, width=column_box[2])

        # Recording the column index and item id
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_id = selected_id

        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)

        entry_edit.focus()
        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        entry_edit.place(x=column_box[0], y=column_box[1], w=column_box[2], h=column_box[3])
        print(column_box)

    def on_enter_pressed(self, event):
        new_text = event.widget.get()

        selected_id = event.widget.editing_item_id

        column_index = event.widget.editing_column_index

        if column_index == -1:
            return
        else:
            current_values = self.item(selected_id).get("values")
            current_values[column_index] = new_text
            self.item(selected_id, values=current_values)

        event.widget.destroy()

    def on_focus_out(self, event):
        event.widget.destroy()


def seek_trial_value(trial_val):
    seek(trial_val)


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


def load_trial_data():
    csv_address = filedialog.askopenfilename()
    csv_data = pd.read_csv(csv_address)
    pack_tree_with_csv(csv_data)


def save_edits_trial_data():
    save_address = tk.filedialog.askopenfilename()
    row_list = []
    columns = ['Trial', 'Start Time', 'Trial?', 'Number Reaches', 'Reach Start Time', 'Reach Stop Time',
               'Handedness', 'Tug of War']
    for row in tree.get_children():
        row_list.append(tree.item(row)["values"])
    treeview_df = pd.DataFrame(row_list, columns=columns)
    treeview_df.to_csv(save_address, index=False)


# Button to load in csv file from path, button for saving csv file, can assume file exists already ie. filedialog

root = tk.Tk()
root.title("Tkinter media")

tree = TEdit(root, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8"), show='headings', height=5)

tree.column("# 1", anchor=CENTER, width=70)
tree.heading("# 1", text="Trial Number")
tree.column("# 2", anchor=CENTER, width=70)
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

# Load Video Button
load_btn = tk.Button(root, text="Load", command=load_video)
load_btn.pack(side='left')

load_csv_btn = tk.Button(root, text="Load CSV", command=load_trial_data)
load_csv_btn.pack(side='left')

update_button = tk.Button(root, text="Update Record", command=save_edits_trial_data())
update_button.pack()

# define video player


# add method for saving outputs in right side

# add method for selecting behavior w/ mouse input


root.mainloop()

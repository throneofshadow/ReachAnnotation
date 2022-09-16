import pdb

import pandas as pd
import numpy as np

header = ['Trial', 'Start Time', 'Trial?', 'Number Reaches', 'Reach Start Time', 'Reach Stop Time',
          'Handedness', 'Tug of War']
trials = np.arange(0, 25, 1)
start_times = np.zeros(25)
start_times[0:5] = [500, 1000, 1500, 2000, 2500]
reach_start_times = np.zeros(25)
trial_class = np.zeros(25)
number_reaches = np.zeros(25)
handedness = np.zeros(25)
tug_of_war = np.zeros(25)
data = np.array([trials, start_times, trial_class, number_reaches, reach_start_times, reach_start_times, handedness, tug_of_war]).T
sim_df = pd.DataFrame(data, columns=header)
sim_df.to_csv('trial_times.csv', index=False)
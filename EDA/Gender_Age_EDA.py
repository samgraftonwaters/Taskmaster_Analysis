import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import Further_Scores_Functions as FSF

plt.rcParams['figure.figsize'] = (13, 7)

file_path = '/Users/SamWaters/Documents/Data Science/Taskmaster/Data/'

gender_age_table = pd.read_csv(file_path + 'Contestent_Gender_Age.csv')


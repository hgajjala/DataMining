%matplotlib inline
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
#plt.rcParams['figure.figsize'] = (16, 9)
#plt.style.use('ggplot')
# Importing the dataset
data = pd.read_csv('C:\General\Big Data\MCS-DS\CS 412 Introduction to DataMining\Assignments\Assignment-3\Assignment-3')
print(data.shape)
data.head()
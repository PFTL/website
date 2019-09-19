import numpy as np
import pandas as pd

data = np.linspace(0, 10, 11)
other_data = np.arange(10, 20, 1)

data_frame = pd.DataFrame(data=[data, other_data])

print(data_frame)
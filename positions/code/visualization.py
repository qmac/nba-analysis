import json

import pandas as pd
import numpy as np

# Helper methods needed to setup visualization

def predictions_to_json(predictions):
    axes = ['G', 'G-F', 'F-G', 'F', 'F-C', 'C-F', 'C']
    seasons = [{'className': row[1]['season'], 'axes':[{'axis': axis, 'value': row[1][axis]} for axis in axes]} for row in predictions.iterrows()]
    print seasons

    with open('./../visualization/positions.json', 'w+') as outfile:
        json.dump(seasons, outfile)
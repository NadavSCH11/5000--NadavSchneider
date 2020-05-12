
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

import base64
import datetime
import io
import re
from os import path

# -------------------------------------------------------------------------------
# Function to convert a plot to an image that can be integrated into an HTML page
# -------------------------------------------------------------------------------
def plot_to_img(fig):
    pngImage = io.BytesIO()
    FigureCanvas(fig).print_png(pngImage)
    pngImageB64String = "data:image/png;base64,"
    pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')
    return pngImageB64String

# -------------------------------------------------------------------
# Function that gets the possible countries for selection by the user
# -------------------------------------------------------------------
def get_country_choices():
    df_short_state = pd.read_csv(path.join(path.dirname(__file__), "..\\static\\Data\\GlobalLandTemperaturesByMajorCity.csv"))
    s = df_short_state.set_index('Country')
    df1 = df_short_state.groupby('Country').sum()
    l = df1.index
    m = list(zip(l , l))
    return m
# -------------------------------------------------------------------------
# Function that gets seperates the day, month and year and returns the year
# -------------------------------------------------------------------------
def get_year(str):
    l = str.split('-')
    return l[0]


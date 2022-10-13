from dash import dash, html, dcc
from dash.dependencies import Input, Output, State
import pandas as pd
import numpy as np

df18 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths18.sas7bdat", encoding='iso-8859-1')
df18['year'] = 2018
df19 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths19.sas7bdat", encoding='iso-8859-1')
df19['year'] = 2019
df20 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths20.sas7bdat", encoding='iso-8859-1')
df20['year'] = 2020
df21 = pd.read_sas("/Users/jamesswank/Downloads/tricountydeaths21.sas7bdat", encoding='iso-8859-1')
df21['year'] = 2021
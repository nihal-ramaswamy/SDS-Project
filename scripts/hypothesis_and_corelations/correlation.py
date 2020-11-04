# -*- coding: utf-8 -*-
"""PopulationAnalysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b8j-aRgj52F4fnuPFtpi-whHa7M-nzj5
"""

import pandas as pd
import matplotlib.pyplot as plt
from statistics import mean

df = pd.read_csv("../../datasets/Full/players_20.csv", encoding="cp1252")

df=df.dropna()

def bestFitLine(xs, ys):
    m = (((mean(xs)*mean(ys)) - mean(xs*ys)) /
         ((mean(xs)*mean(xs)) - mean(xs*xs)))
    
    b = mean(ys) - m*mean(xs)
    
    regression_line = []
    for x in xs:
        regression_line.append((m*x)+b)
    return regression_line

fig, ax = plt.subplots(figsize = (10, 5))


x = df[df['team_position'] == 'ST']['shooting']
y = df[df['team_position'] == 'ST']['overall']

plt.scatter(x, y) 
plt.plot(x, bestFitLine(x, y), color = 'red')
plt.xlabel('Shooting')
plt.ylabel('Overall')
plt.title('Shooting vs Overall')
plt.show()

fig, ax = plt.subplots(figsize = (10, 5))


x = df[df['team_position'] == 'SUB']['weight_kg']
y = df[df['team_position'] == 'SUB']['age']

plt.scatter(x, y) 
plt.plot(x, bestFitLine(x, y), color = 'red')
plt.xlabel('Weight')
plt.ylabel('Age')
plt.title('Age vs Weight')
plt.show()

"""**Try finding a negative correlation**"""
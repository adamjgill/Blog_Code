import pandas as pd
from bokeh.plotting import figure, show, output_file

#creating the file the graph will write to
output_file("WindGraph.html")

#Importing CSV's and changing column names, header=0 replaces column names in first row
windOver100 = pd.read_csv('windOver100.csv', header=0, names=['date', 'WindOver100'])
avgWind     = pd.read_csv('avgWind.csv', header=0, names=['date','AvgWind'])

#Converting the date column to a readable datetime format
windOver100.date = pd.to_datetime(windOver100.date)
avgWind.date     = pd.to_datetime(avgWind.date)

#merging database and getting rid duplicats as well as ordering by the date
mergedDataframe = pd.merge(avgWind, windOver100, how='inner', on='date')
mergedDataframe = mergedDataframe.drop_duplicates(subset='date')
mergedDataframe = mergedDataframe.sort_values(by=['date'])

#The rolling average itself
mergedDataframe['RollingAvg'] = mergedDataframe.AvgWind.rolling(90).mean() #90 can be changed to any number, this blog used 90 and 365
mergedDataframe['RollingSum'] = mergedDataframe.WindOver100.rolling(90).sum()

#Creating the figure itself
p = figure(x_axis_type="datetime", title="Average Winds vs 100 mph days", width=1200)
p.line(mergedDataframe['date'], mergedDataframe['RollingAvg'], legend="Wind Rolling 90 day Average")
p.line(mergedDataframe['date'], mergedDataframe['RollingSum'], color='red', legend="Rolling 90 day Sum of Days > 100 MPH")
p.legend.location = "bottom_left"
p.xaxis.axis_label = "Date"
p.yaxis.axis_label = "Number of Occurances / Yearly wind average"

show(p)

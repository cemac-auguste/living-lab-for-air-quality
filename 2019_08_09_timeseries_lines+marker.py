#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:13:03 2019

@author: earaza
"""
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot as pop


path_to_data = '/nfs/see-fs-02_users/earaza/Desktop'
file_name = "august9.csv"
full_file_name = '/'.join([path_to_data, file_name])
print('AZ: ', full_file_name)
data = pd.read_csv(full_file_name, sep=',', header='infer', na_values='NaN')
df_1 = data[['time', 'sds02-pm2.5', 'sds02-pm10', 'sds02-TSP', 'sds04-pm2.5', 'sds04-pm10', 'sds04-TSP']]

datetimes = pd.to_datetime(df_1['time'])

labels = []
for i in range(len(data['lat'])):
    labels.append('Lat: {}, Lon: {}'.format(data['lat'][i], data['lon'][i]))

fig = go.Figure()
for sensor in ['sds02-pm2.5', 'sds04-pm2.5']:
    fig.add_trace(go.Scatter(x=datetimes, y=df_1[sensor], mode='lines+markers', opacity=0.7, name='{}'.format(sensor), text=labels))
fig.update_layout(title_text='Campus Walk (09/08/2019) by Auguste Zagorskaite', xaxis_rangeslider_visible=True)

pop(fig, filename='graph.html', output_type='file', show_link=False, auto_open=True, include_plotlyjs=True)
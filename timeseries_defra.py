#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:15:43 2019

@author: earaza
"""
import pandas as pd
import plotly.graph_objs as go
from plotly.offline import plot as pop


path_to_data = '/nfs/see-fs-02_users/earaza/Desktop'
file_name = "20190819_11:04-11:22_defra_monitoring_site_city_centre.csv"
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

for sensor_1 in ['sds02-pm10', 'sds04-pm10']:
    fig.add_trace(go.Scatter(x=datetimes, y=df_1[sensor_1], mode='lines+markers', opacity=0.7, name='{}'.format(sensor_1), text=labels))
fig.update_layout(title_text='TIme Series for data gathered near Defra Monitoring Site in the cty centre of Leeds (19/08/2019) by Auguste Zagorskaite', xaxis_rangeslider_visible=True)
pop(fig, filename='time_series_defra.html', output_type='file', show_link=False, auto_open=True, include_plotlyjs=True)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:40:06 2019

@author: earaza
"""

import pandas as pd

#Read data from file 'august7.csv'
path_to_data = '/nfs/see-fs-02_users/earaza/Desktop'
file_name = "august7.csv"
full_file_name = '/'.join([path_to_data, file_name])
print('AZ: ', full_file_name)
data = pd.read_csv(full_file_name, sep=',', header='infer', na_values='NaN')

df_1 = data[['time', 'lat', 'lon', 'alt', 'sds02-pm2.5', 'sds02-pm10', 'sds02-TSP', 'sds04-pm2.5', 'sds04-pm10', 'sds04-TSP']]
print('AZ: city walk by Auguste Zagorskaite')
print('Head of data frame', df_1.head()) 
print('Tail of data frame', df_1.tail())

df = df_1.dropna()
print('Head of data frame', df.head()) 
print('Tail of data frame', df.tail())
print("Length of filtered dataframe:",len(df))


html_page = []
ScriptHtml = []

begTagHtml = '<html>'
endTagHtml = '</html>'

newline="\n"

begTagHead='<head>'
endTagHead='</head>'

begTagBody = '<body>'
endTagBody = '</body>'
titleHtml='<title> City Walk 3 by Auguste </title>'

HeadHtml="""
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	
	<link rel="shortcut icon" type="image/x-icon" href="docs/images/favicon.ico" />

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css" integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ==" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js" integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og==" crossorigin=""></script>

"""
DivHtml="""
<div id="mapid" style="width: 1000px; height: 900px;"></div>
"""
ScriptContent="""

	var mymap = L.map('mapid').setView([53.8008, -1.5491], 13);
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery � <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox.streets'
	}).addTo(mymap);

"""

print("Length of data frame= ", len(df['time']))

A_Circle=""
for a in range(len(df)):
    circle_lat = df['lat'][a]
    circle_lon = df['lon'][a]
    circle_2_pm2p5 = df['sds02-pm2.5'][a]
    circle_4_pm2p5 = df['sds04-pm2.5'][a]
    circle_js_pm2p5 = "L.circle([{}, {}], {{color: 'green', fillColor: '0#f3', fillOpacity: 0.2, radius: 20}}).bindPopup('<b>Sensor 2, Sensor 4 values (pm2.5)</b><br>{}, {}').addTo(mymap);\n".format(circle_lat, circle_lon, circle_2_pm2p5, circle_4_pm2p5)
    A_Circle = '{} {}'.format(A_Circle, circle_js_pm2p5)


B_Circle=""
for b in range (len(df)):
    circle_lat = df['lat'][b]
    circle_lon = df['lon'][b]
    circle_2_pm10 = df['sds02-pm10'][b]
    circle_4_pm10 = df['sds04-pm10'][b]
    circle_js_pm10 = "L.circle([{}, {}], {{color: 'yellow', fillColor: '0#f3', fillOpacity: 0.2, radius: 15}}).bindPopup('<b>Sensor 2, Sensor 4 values (pm10)</b><br>{}, {}').addTo(mymap);\n".format(circle_lat, circle_lon, circle_2_pm10, circle_4_pm10)
    B_Circle = '{} {}'.format(B_Circle, circle_js_pm10)

C_Circle=""
for c in range (len(df)):
    circle_lat = df['lat'][c]
    circle_lon = df['lon'][c]
    circle_2_tsp = df['sds02-TSP'][c]
    circle_4_tsp = df['sds04-TSP'][c]
    circle_js_tsp = "L.circle([{}, {}], {{color: 'red', fillColor: '0#f3', fillOpacity: 0.2, radius: 10}}).bindPopup('<b>Sensor 2, Sensor 4 values (TSP)</b><br>{}, {}').addTo(mymap);\n".format(circle_lat, circle_lon, circle_2_tsp, circle_4_tsp)
    C_Circle = '{} {}'.format(C_Circle, circle_js_tsp)
    
clickFunc="""
function onMapClick(e) {
        alert("You clicked the map at " + e.latlng);
}
mymap.on('click', onMapClick);
"""

#SetInitialZoom="""
#mymap.fitBounds(circle.getBounds());
#"""

ScriptHtml.append('<script>')
ScriptHtml.append(ScriptContent)
ScriptHtml.append(A_Circle)
ScriptHtml.append(B_Circle)
ScriptHtml.append(C_Circle)
ScriptHtml.append(clickFunc)
#ScriptHtml.append(SetInitialZoom)
ScriptHtml.append('</script>')

CompleteScript=newline.join(ScriptHtml)

html_page.append(begTagHtml)
html_page.append(begTagHead)
html_page.append(titleHtml)
html_page.append(HeadHtml)
html_page.append(endTagHead)
html_page.append(begTagBody)
html_page.append(DivHtml)
html_page.append(CompleteScript)
html_page.append(endTagBody)
html_page.append(endTagHtml)

###print("DBG: ",html_page)

soup = newline.join(html_page)
###print("DBG: ",soup)

with open("august7walk_3.html", "w", encoding='utf-8') as file:
    file.write(str(soup))
print('End of script')
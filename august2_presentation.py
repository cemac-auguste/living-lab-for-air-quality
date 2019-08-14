#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:15:32 2019

@author: earaza
"""

import pandas as pd

# MRI use a generic function to create a new layer from a dataframe df_v
def create_layer_from_dataframe(df_v,label_s, popup_s,group_s,attrib):
    '''
       Usage: (dataframe, column label_string, associated popup string) .
       This function assumes the valid dataframe, df_v, has the structure
           time, lat, lon, alt, value1,value2,value3
       the values in columns 4-6 (zero-indexed) are triplet from a particular sensor
       repeated for up to 4 sensors (or more is daisy chaining USB
    '''
    # declare the string to be returned
    layer_string=""
    # decode the attributes for use in the layer value
    color, radius, transp, thickness = attrib
    # thickness can be fillcolor
    
    print("DEBUG:",color,radius, transp, thickness)
    # now fill the string
    for a in range(len(df_v)):
        lyr_lat = df_v['lat'][a]
        lyr_lon = df_v['lon'][a]
        # the label_s string selects the column of df_v to be processed
        # CAUTION to make sure apostrophes are preserved to make the color string a string in JS
        layer_values = "L.circle([{}, {}], {{color: '{}', fillColor: '0#f3', fillOpacity: {}, radius: {}}}).bindPopup('<b>{}</b><br>{}, {}, {}').addTo({});\n".format(lyr_lat, lyr_lon, color, transp, radius, popup_s, lyr_lat,lyr_lon,df_v[label_s][a],group_s)
        layer_string = '{} {}'.format(layer_string, layer_values)
   

    return layer_string

#Read data from file 'august7.csv'
path_to_data = '/nfs/see-fs-02_users/earaza/Desktop'
file_name = "august2_adjusted.csv"
full_file_name = '/'.join([path_to_data, file_name])
print('AZ: ', full_file_name)
data = pd.read_csv(full_file_name, sep=',', header='infer', na_values='NaN')

df_1 = data[['time', 'lat', 'lon', 'alt', 'sds02-pm2.5', 'sds02-pm10', 'sds02-TSP', 'sds04-pm2.5', 'sds04-pm10', 'sds04-TSP']]
print('AZ: campus walk by Auguste Zagorskaite')
print('Head of data frame', df_1.head()) 
print('Tail of data frame', df_1.tail())

##Filter out the nans from the dataframe
##AZ Homework is to look up pandas

df = df_1.dropna()
###mri print('Head of data frame', df.head()) 
###mri print('Tail of data frame', df.tail())
print("Length of filtered dataframe:",len(df))
print("Length of data frame= ", len(df['time']))


html_page = []
ScriptHtml = []

begTagHtml = '<html>'
endTagHtml = '</html>'

newline="\n"

begTagHead='<head>'
endTagHead='</head>'

begTagBody = '<body>'
endTagBody = '</body>'
titleHtml='<title> Campus Walk 1 by Auguste </title>'

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

# MRI changing the way the map is defined to match layer control tutorial
AccessTiles="""

    var mbURL = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';

    var mbAttrib = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
                   '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
                   'Imagery � <a href="https://www.mapbox.com/">Mapbox</a>'

    var streets = L.tileLayer(mbURL, { id: 'mapbox.streets', maxZoom: 18, attribution: mbAttrib} )

"""

PrepareCanvas = """
    var mymap = L.map('mapid', {
                      center: [53.8008, -1.5491], 
                      zoom: 13,
                      layers:[streets,GroupA,GroupB,GroupC,GroupD]
    });
"""

A_Circle=""
A_declare_group ="""
var GroupA = L.layerGroup();
"""
A_Attributes = [ 'red','20','0.2','0.1']
A_Circle = create_layer_from_dataframe(df,'sds02-pm2.5','Sensor2 pm2.5','GroupA',A_Attributes)

B_Circle=""
B_Attributes = [ 'blue','16','0.2','0.1']
B_Circle = create_layer_from_dataframe(df,'sds02-pm10','Sensor 2 pm10','GroupB',B_Attributes)
B_declare_group = """
var GroupB = L.layerGroup();
"""
C_declare_group ="""
var GroupC = L.layerGroup();
"""
D_declare_group ="""
var GroupD = L.layerGroup();
"""

# MRI wait to use C and D when A and B work
C_Circle=""
C_Attributes = [ 'yellow','12','0.2','0.1']
C_Circle = create_layer_from_dataframe(df,'sds04-pm2.5','Sensor 4 pm2.5','GroupC',C_Attributes)
    
D_Circle=""
D_Attributes = [ 'green','8','0.2','0.1']
D_Circle = create_layer_from_dataframe(df,'sds04-pm10','Sensor 4 PM10','GroupD',D_Attributes)

# compound the layers for user layer selection
layer_cntl = """
             var baseMaps = {
                 "Streets": streets
             };
             var SensorLayer = {
                 "Sensor 2 pm2.5": GroupA,
                 "Sensor 2 pm10 ": GroupB,
                 "Sensor 4 pm2.5": GroupC,
                 "Sensor 4 pm10 ": GroupD
             };
                 
             L.control.layers(baseMaps,SensorLayer).addTo(mymap);\n
"""

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
ScriptHtml.append(AccessTiles)
ScriptHtml.append(A_declare_group)
ScriptHtml.append(B_declare_group)
ScriptHtml.append(C_declare_group)
ScriptHtml.append(D_declare_group)
ScriptHtml.append(PrepareCanvas)
ScriptHtml.append(A_Circle)
ScriptHtml.append(B_Circle)
ScriptHtml.append(C_Circle)
ScriptHtml.append(D_Circle)
ScriptHtml.append(layer_cntl)
ScriptHtml.append(clickFunc)
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

with open("august2_presentation.html", "w", encoding='utf-8') as file:
    file.write(str(soup))
print('End of script')
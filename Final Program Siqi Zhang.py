"""
Name:       Siqi Zhang
CS230:      Section 4
Data:       Airports around the World
URL:        Link to your web application on Streamlit Cloud (if posted) 

Description:
This program includes a bunch of streamlit and pandas features we learned or skipped in class: streamlit, pydeck, pandas, numpy, plt, time.
"""

import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

st.set_option('deprecation.showPyplotGlobalUse', False)

st.title(':blue[G]:red[l]:green[o]:blue[b]:green[a]:red[l] :blue[A]:red[i]:green[r]:blue[p]:green[o]:red[r]:blue[t]:red[s] :earth_americas: :airplane:')

df_read = pd.read_csv('airport-codes_csv.csv', keep_default_na = False)
df_airport = pd.DataFrame(df_read)

def unique_value(list, modification = 'remain'):
    empty_list = []
    for i in list:
        if i not in empty_list:
            if modification == 'U':
                empty_list.append(i.upper())
            elif modification == 'L':
                empty_list.append(i.lower())
            else:
                empty_list.append(i)
    sorted_empty_list = sorted(empty_list)
    return empty_list, sorted_empty_list

# Continent
airport_continent, sorted_airport_continent = unique_value(df_airport.continent)
airport_continent_dict = {'All': 'All', 'AF': 'Africa', 'AN': 'Antarctica', 'AS': 'Asia', 'EU': 'Europe', 'NA': 'North America', 'OC': 'Oceania', 'SA': 'South America'}
selected_continent = st.selectbox('Please select a continent:', list(airport_continent_dict.values()))
for i in airport_continent_dict:
    if airport_continent_dict[i] == selected_continent:
        selected_continent_short = i
if selected_continent_short != 'All':
    df_airport = df_airport[df_airport['continent'] == selected_continent_short]
st.write(f'{len(df_airport)} airports found in {selected_continent} continent.')

# Country
airport_country, sorted_airport_country = unique_value(df_airport.iso_country)
sorted_airport_country.insert(0, 'All')
selected_country = st.selectbox('Please select a country:', sorted_airport_country)
if selected_country != 'All':
    df_airport = df_airport[df_airport['iso_country'] == selected_country]
st.write(f'{len(df_airport)} airports found in {selected_country}, {selected_continent} continent.')

# Type
airport_type, sorted_airport_type = unique_value(df_airport.type)
airport_type_dict = {'All': 'All', 'small_airport': 'Small airport', 'medium_airport': 'Medium airport', 'large_airport': 'Large airport', 'heliport': 'Heliport', 'seaplane_base': 'Seaplane base', 'balloonport': 'Balloonport', 'closed': 'Closed airport'}
selected_type = st.selectbox('Please select a type:', list(airport_type_dict.values()))
for i in airport_type_dict:
    if airport_type_dict[i] == selected_type:
        selected_type_short = i
if selected_type_short != 'All':
    df_airport = df_airport[df_airport['type'] == selected_type_short]
st.write(f'{len(df_airport)} {selected_type}s found in {selected_country}, {selected_continent} continent.')

st.header('Data')
column_dict = {'Type': 'type', 'Elevation Ft.': 'elevation_ft', 'Continent': 'continent', 'Country': 'iso_country', 'Region': 'iso_region', 'Municipality': 'municipality', 'GPS Code': 'gps_code', 'IATA Code': 'iata_code', 'Local Code': 'local_code', 'Coordinates': 'coordinates'}
selected_column = st.multiselect('Columns Displayed:', list(column_dict.keys()))
df_airport_duplicate = df_airport.copy()
selected_column_list = ['ident', 'name']
for i in selected_column:
    selected_column_list.append(column_dict[i])
df_airport_duplicate.index = df_airport_duplicate.index + 1
st.write(df_airport_duplicate[selected_column_list])



# Pivot Table
pivot = pd.pivot_table(data = df_airport, index = ['continent'], columns = ['type'], values = ['elevation_ft'], aggfunc = np.mean)



# Bar Chart
st.header('Bar Chart')
airport_type = ['small_airport', 'medium_airport', 'large_airport', 'heliport', 'seaplane_base', 'balloonport', 'closed']
amount_list = []
for type in airport_type:
    amount = len(df_airport[df_airport['type'] == type])
    amount_list.append(amount)
type_data = {'type': airport_type, 'amount': amount_list}
df_type = pd.DataFrame(type_data)
df_type.plot(kind = 'bar', x = 'type', y = 'amount')
plt.xlabel('Type')
plt.ylabel('Amount')
plt.title('Bar Chart for Airport Type')
st.pyplot()

# Pie Chart
st.header('Pie Chart')
df_type.plot(kind = 'pie', y = 'amount')
plt.title('Pie Chart for Airport Type')
st.pyplot()



# Map
NORMAL_AIRPORT_URL = 'https://upload.wikimedia.org/wikipedia/commons/f/fa/Airport_icon_small.png'
normal_airport_icon_data = {
        "url": NORMAL_AIRPORT_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }
HELIPORT_URL = 'https://upload.wikimedia.org/wikipedia/commons/3/32/Helicopter-black-icon.svg'
heliport_icon_data = {
        "url": HELIPORT_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }
SEAPLANEBASE_URL = 'https://upload.wikimedia.org/wikipedia/commons/5/59/Pictograms-nps-misc-sea_plane-2.svg'
seaplanebase_icon_data = {
        "url": SEAPLANEBASE_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }
BALLOONPORT_URL = 'https://upload.wikimedia.org/wikipedia/commons/f/f5/Toicon-icon-stone-float.svg'
balloonport_icon_data = {
        "url": BALLOONPORT_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }
CLOSED_URL = 'https://upload.wikimedia.org/wikipedia/commons/f/f5/Toicon-icon-lines-and-angles-halt.svg'
closed_icon_data = {
        "url": CLOSED_URL,
        "width": 100,
        "height": 100,
        "anchorY": 100
        }

df_airport['lat'] = None
df_airport['lon'] = None
df_airport['icon_data'] = None
for i in df_airport.index:
    coordinate_list = df_airport['coordinates'][i].split(', ')
    df_airport['lat'][i] = round(float(coordinate_list[1]), 6)
    df_airport['lon'][i] = round(float(coordinate_list[0]), 6)
    if df_airport['type'][i] == 'small_airport' or df_airport['type'][i] == 'medium_airport' or df_airport['type'][i] == 'large_airport':
        df_airport['icon_data'][i] = normal_airport_icon_data
    elif df_airport['type'][i] == 'heliport':
        df_airport['icon_data'][i] = heliport_icon_data
    elif df_airport['type'][i] == 'seaplane_base':
        df_airport['icon_data'][i] = seaplanebase_icon_data
    elif df_airport['type'][i] == 'balloonport':
        df_airport['icon_data'][i] = balloonport_icon_data
    elif df_airport['type'][i] == 'closed':
        df_airport['icon_data'][i] = closed_icon_data

icon_layer = pdk.Layer(type = 'IconLayer',
                       data = df_airport,
                       get_icon = 'icon_data',
                       get_position = '[lon, lat]',
                       get_size = 4,
                       size_scale = 10,
                       pickable = True)

view_state = pdk.ViewState(latitude = df_airport['lat'].mean(),
                           longitude = df_airport['lon'].mean(),
                           zoom = 3,
                           pitch = 0)

tool_tip = {'html': 'Airport Name:<br/><b>{name}</b>'
                    '',
            'style': {'backgroundColor': 'white',
                      'color': 'black'}}

icon_map = pdk.Deck(map_style = 'mapbox://styles/mapbox/streets-v12',
                    initial_view_state = view_state,
                    layers = icon_layer,
                    tooltip = tool_tip)

st.header('Map')
st.pydeck_chart(icon_map)

times = 0
while times < 10:
    times += 1
    st.text('')

# Others
st.header('Q&A')
st.image('https://uploads-ssl.webflow.com/5fd1ff04a1e777f1f75cf766/5fdb84b262bb06b94cf6ed7b_5e0976a4ad6badd4a4bd315c_qa-header%25402x.png')

times = 0
while times < 10:
    times += 1
    st.text('')

st.header('Grade My Project :100:')
grade = st.slider('Grading Slider', min_value = 0, max_value = 100, step = 1, value = 0)
if grade < 65:
    st.write(f'You grade is {grade}%. You get F.')
elif grade < 66:
    st.write(f'You grade is {grade}%. You get D.')
elif grade < 69:
    st.write(f'You grade is {grade}%. You get D+.')
elif grade < 72:
    st.write(f'You grade is {grade}%. You get C-.')
elif grade < 76:
    st.write(f'You grade is {grade}%. You get C.')
elif grade < 79:
    st.write(f'You grade is {grade}%. You get C+.')
elif grade < 82:
    st.write(f'You grade is {grade}%. You get B-.')
elif grade < 86:
    st.write(f'You grade is {grade}%. You get B.')
elif grade < 89:
    st.write(f'You grade is {grade}%. You get B+.')
elif grade < 92:
    st.write(f'You grade is {grade}%. You get A-.')
elif grade < 96:
    st.write(f'You grade is {grade}%. You get A. Congrats!')
elif grade <= 100:
    st.write(f'You grade is {grade}%. You get A+. Congrats!')

st.text_area('Leave a comment if you want: ')

if grade >= 96:
    for count in range(10):
        st.balloons()
        time.sleep(3)
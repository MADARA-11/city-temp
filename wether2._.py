import matplotlib.pyplot as plt
import streamlit as st
import json
import requests
import pandas as pd

st.title("Weather app 🌥️")
st.subheader("enter a city name to get the current weather or the forecast ")

api_key = "9bdc5b38d8694d09b1c121938251403"

option = st.radio('choose an option',['current Weather ','Forecast'])

if option == "current Weather ":
    city = st.text_input('Enter the city name.')

    if st.button('Display'):
        base_url = f"http://api.weatherapi.com/v1/current.json?key=9bdc5b38d8694d09b1c121938251403&q={city}&aqi=no"

        p = {
            "appid": api_key,
            "q": city
            }

        respones = requests.get(base_url, params=p)

        # st.write(respones.json())

        if respones.status_code == 200:
            data = respones.json()
            pic = data['current']['condition']['icon']
            pic = 'https:' + pic

            st.image(pic, width= 100)
            st.subheader(f"☁️Weather info on {city}")
            st.subheader(f"⏲️local data and time :{data['location']['localtime']}")
            st.write(f"🕛🔥Temperature in celsius:{data["current"]["temp_c"]}")
            st.write(f"🔥Temperature in fahrenheit:{data["current"]["temp_f"]}")
            st.write(f'☁️ weather feels like :{data["current"]["condition"]["text"]}')
            st.write(f'☁️ the wind speed in kph  :{data["current"]["wind_kph"]}')
            st.write(f'☁️ the humidity in that area :{data["current"]["humidity"]}')
            st.write(f"🌎location or the region {data["location"]["region"]}")
            st.subheader("City on map🗺️")
            lat =data['location']['lat']
            lon = data['location']['lon']
            dix = {"lat":[lat],"lon":[lon]}
            x = pd.DataFrame(dix)
            st.map(x)
        else:
            st.error("Enter a proper city name ..................")

if option == "Forecast":
    city = st.text_input('Enter the city name ')
    days = st.number_input('Enter the no. of days', min_value= 1)
    base_url = f"http://api.weatherapi.com/v1/forecast.json?key=50ab1bfa0fa44103afd124805251104&q={city}&days={days}&aqi=no&alerts=no"
    respones = requests.get(base_url)

    if respones.status_code == 200:
        data = respones.json()
        days = data['forecast']['forecastday']
        t = days[0]['hour']

        time_list = []
        temp_list = []

        for i in t:
            time_list.append(i['time'])
            temp_list.append(i['temp_c'])


        fig = plt.figure(figsize=(10,6))
        plt.plot(time_list,temp_list,marker = 'o',color = 'green')
        plt.xticks(rotation = 90)
        plt.grid()
        plt.xlabel('Time')
        plt.ylabel("Temp in celcius")
        plt.title(f"Temperature forecast of {city}")
        
        if st.button("Display Graph"):

            st.pyplot(fig)
            st.subheader("City on map🗺️")
            lat = data['location']['lat']
            lon = data['location']['lon']
            dix = {"lat": [lat], "lon": [lon]}
            x = pd.DataFrame(dix)
            st.map(x)
    else:
        st.error("Enter a proper city name ..................")

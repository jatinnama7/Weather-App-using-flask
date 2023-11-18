from flask import Flask, render_template, request, jsonify
from tkinter import *
import tkinter as tk
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_code', methods=['POST'])
def run_code():
    try:
        city = request.json.get('city', '')
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

        home = pytz.timezone(result)
        location_time = datetime.now(home)
        current_time = location_time.strftime("%I:%M %p")

        api = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=6e6e47512147263887b8d9294199fd62"
        json_data = requests.get(api).json()
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        result_data = {
            'current_time': current_time,
            'condition': condition,
            'description': description,
            'temp': temp,
            'pressure': pressure,
            'humidity': humidity,
            'wind': wind
        }

        return jsonify(result_data)

    except Exception as e:
        return jsonify({'error': 'Invalid Entry!'})

if __name__ == '__main__':
    app.run(debug=True)

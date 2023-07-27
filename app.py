import requests
from flask import Flask, render_template, request
import os

app = Flask(__name__)

API_URL = "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"

def get_weather_data(date):
    data = fetch_api_data()
    for entry in data['list']:
        if entry['dt_txt'] == date:
            return entry['main']['temp']
    return None

def get_wind_speed_data(date):
    data = fetch_api_data()
    for entry in data['list']:
        if entry['dt_txt'] == date:
            return entry['wind']['speed']
    return None

def get_pressure_data(date):
    data = fetch_api_data()
    for entry in data['list']:
        if entry['dt_txt'] == date:
            return entry['main']['pressure']
    return None

def fetch_api_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        return {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        choice = request.form['choice']

        if choice == '1':
            return render_template('get_weather.html')
        elif choice == '2':
            return render_template('get_wind_speed.html')
        elif choice == '3':
            return render_template('get_pressure.html')
        elif choice == '0':
            result = "Exiting the program."
            os._exit(0)  # Gracefully stop the Flask server
        else:
            result = "Invalid choice. Please try again."
            return render_template('index.html', result=result)

    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    date = request.form['date']
    weather = get_weather_data(date)

    if weather is not None:
        result = f"Temperature on {date}: {weather:.2f}°C"
    else:
        result = "Data not found for the given date."

    return render_template('result.html', result=result)

@app.route('/get_wind_speed', methods=['POST'])
def get_wind_speed():
    date = request.form['date']
    wind_speed = get_wind_speed_data(date)

    if wind_speed is not None:
        result = f"Wind Speed on {date}: {wind_speed:.2f} m/s"
    else:
        result = "Data not found for the given date."

    return render_template('result.html', result=result)

@app.route('/get_pressure', methods=['POST'])
def get_pressure():
    date = request.form['date']
    pressure = get_pressure_data(date)

    if pressure is not None:
        result = f"Pressure on {date}: {pressure:.2f} hPa"
    else:
        result = "Data not found for the given date."

    return render_template('result.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)

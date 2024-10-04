from flask import Flask, render_template, request, redirect, url_for
import urllib.request
import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        city = request.form['city']
        return redirect(url_for('get_weather', city=city))
    return render_template('home.html')

@app.route('/forecast', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    if city is None:
        return redirect(url_for('home'))
    
    api_key = '75a48edfb84f753cc0d738d2e7925a27'
    base_url = 'http://api.openweathermap.org/data/2.5/forecast'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }

    try:
        full_url = f"{base_url}?{urllib.parse.urlencode(params)}"
        print(f"Requesting URL: {full_url}")  # Debug print
        
        with urllib.request.urlopen(full_url) as response:
            raw_data = response.read()
            print(f"Raw API response: {raw_data}")  # Debug print
            weather_data = json.loads(raw_data)

        if 'list' not in weather_data:
            print(f"Unexpected API response structure: {weather_data}")  # Debug print
            return "Unexpected response from weather API", 500

        processed_data = {
            'city': weather_data['city']['name'],
            'country': weather_data['city']['country'],
            'forecasts': []
        }

        for item in weather_data['list'][:5]:  # Get first 5 forecasts
            forecast = {
                'datetime': item['dt_txt'],
                'temperature': item['main']['temp'],
                'description': item['weather'][0]['description'],
                'icon': item['weather'][0]['icon']
            }
            processed_data['forecasts'].append(forecast)

        return render_template('weather.html', weather=processed_data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} {e.reason}")  # Debug print
        return f"Error fetching weather data: {e.code} {e.reason}", 500
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {str(e)}")  # Debug print
        return "Error processing weather data", 500
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # Debug print
        return "An unexpected error occurred", 500



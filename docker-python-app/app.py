from flask import Flask, render_template_string, request, jsonify
import requests
from datetime import datetime

app = Flask(__name__)

# HTML template with embedded CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weather App 🌤️</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #333;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .search-box {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
        }
        input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        input:focus {
            outline: none;
            border-color: #667eea;
        }
        button {
            padding: 15px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: transform 0.2s;
        }
        button:hover {
            transform: translateY(-2px);
        }
        button:active {
            transform: translateY(0);
        }
        .weather-info {
            text-align: center;
            display: none;
        }
        .weather-info.show {
            display: block;
            animation: fadeIn 0.5s;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .city-name {
            font-size: 2em;
            color: #333;
            margin-bottom: 10px;
        }
        .temperature {
            font-size: 4em;
            font-weight: bold;
            color: #667eea;
            margin: 20px 0;
        }
        .description {
            font-size: 1.5em;
            color: #666;
            text-transform: capitalize;
            margin-bottom: 20px;
        }
        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 30px;
        }
        .detail-item {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
        }
        .detail-label {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 5px;
        }
        .detail-value {
            color: #333;
            font-size: 1.3em;
            font-weight: bold;
        }
        .error {
            color: #e74c3c;
            text-align: center;
            padding: 15px;
            background: #fadbd8;
            border-radius: 10px;
            margin-top: 20px;
            display: none;
        }
        .error.show {
            display: block;
        }
        .loading {
            text-align: center;
            color: #667eea;
            font-size: 1.2em;
            display: none;
        }
        .loading.show {
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌤️ Weather App</h1>
        <div class="search-box">
            <input type="text" id="cityInput" placeholder="Enter city name..." value="London">
            <button onclick="getWeather()">Search</button>
        </div>
        
        <div class="loading" id="loading">Loading...</div>
        <div class="error" id="error"></div>
        
        <div class="weather-info" id="weatherInfo">
            <div class="city-name" id="cityName"></div>
            <div class="temperature" id="temperature"></div>
            <div class="description" id="description"></div>
            <div class="details">
                <div class="detail-item">
                    <div class="detail-label">Feels Like</div>
                    <div class="detail-value" id="feelsLike"></div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Humidity</div>
                    <div class="detail-value" id="humidity"></div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Wind Speed</div>
                    <div class="detail-value" id="windSpeed"></div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Pressure</div>
                    <div class="detail-value" id="pressure"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function getWeather() {
            const city = document.getElementById('cityInput').value;
            if (!city) {
                showError('Please enter a city name');
                return;
            }

            document.getElementById('loading').classList.add('show');
            document.getElementById('error').classList.remove('show');
            document.getElementById('weatherInfo').classList.remove('show');

            fetch(`/weather?city=${encodeURIComponent(city)}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').classList.remove('show');
                    
                    if (data.error) {
                        showError(data.error);
                    } else {
                        displayWeather(data);
                    }
                })
                .catch(error => {
                    document.getElementById('loading').classList.remove('show');
                    showError('Failed to fetch weather data');
                });
        }

        function displayWeather(data) {
            document.getElementById('cityName').textContent = data.city;
            document.getElementById('temperature').textContent = data.temperature;
            document.getElementById('description').textContent = data.description;
            document.getElementById('feelsLike').textContent = data.feels_like;
            document.getElementById('humidity').textContent = data.humidity;
            document.getElementById('windSpeed').textContent = data.wind_speed;
            document.getElementById('pressure').textContent = data.pressure;
            document.getElementById('weatherInfo').classList.add('show');
        }

        function showError(message) {
            document.getElementById('error').textContent = message;
            document.getElementById('error').classList.add('show');
        }

        document.getElementById('cityInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                getWeather();
            }
        });

        // Load default weather on page load
        window.onload = function() {
            getWeather();
        };
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/weather")
def weather():
    city = request.args.get('city', 'London')
    
    # Using OpenWeatherMap API (free tier)
    # You can get a free API key from: https://openweathermap.org/api
    API_KEY = "YOUR_API_KEY_HERE"  # Replace with your API key
    
    try:
        # For demo purposes, returning mock data
        # Uncomment the code below and add your API key to use real data
        
        # url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        # response = requests.get(url, timeout=5)
        # data = response.json()
        
        # if response.status_code == 200:
        #     weather_data = {
        #         'city': data['name'],
        #         'temperature': f"{data['main']['temp']:.1f}°C",
        #         'description': data['weather'][0]['description'],
        #         'feels_like': f"{data['main']['feels_like']:.1f}°C",
        #         'humidity': f"{data['main']['humidity']}%",
        #         'wind_speed': f"{data['wind']['speed']} m/s",
        #         'pressure': f"{data['main']['pressure']} hPa"
        #     }
        #     return jsonify(weather_data)
        # else:
        #     return jsonify({'error': 'City not found'}), 404
        
        # Mock data for demonstration
        mock_data = {
            'city': city.title(),
            'temperature': '18.5°C',
            'description': 'partly cloudy',
            'feels_like': '17.2°C',
            'humidity': '65%',
            'wind_speed': '4.5 m/s',
            'pressure': '1013 hPa'
        }
        return jsonify(mock_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
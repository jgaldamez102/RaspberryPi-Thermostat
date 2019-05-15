import requests
# OpenWeatherMap API: https://openweathermap.org/current
OWM_API_KEY = 'e3106c168cf6e06e1303cb6b2a305bf4'  # OpenWeatherMap API Key
DEFAULT_ZIP = 90007

def get_weather():
    params = {#dict params
        'appid': OWM_API_KEY,#Joses' API key
        'zip' : DEFAULT_ZIP,#use local USC zip rather than 90089
        'units' : 'imperial'#change units
    }
    response = requests.get('http://api.openweathermap.org/data/2.5/weather', params)
    if response.status_code == 200: # Status: OK
        data = response.json()#get data from response
        return data['main']['temp']#index from the dictionary
    else:
        return 0.0

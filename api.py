import requests
import datetime
import json

API_KEY = ''

def get_air_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    resp = requests.get(url)

    message = "Nothing Found."

    if resp.status_code == 200:
        data = json.loads(resp.text)
        components = data['list'][0]['components']
        message = ""
        if components['co'] != '':
            message += "CO: " + str(components['co']) + '\n'
        if components['no'] != '':
            message += "NO: " + str(components['no']) + '\n'
        if components['no2'] != '':
            message += "NO2: " + str(components['no2']) + '\n'
        if components['o3'] != '':
            message += "O3: " + str(components['o3']) + '\n'
        if components['so2'] != '':
            message += "SO2: " + str(components['so2']) + '\n'
        if components['pm2_5'] != '':
            message += "PM25: " + str(components['pm2_5']) + '\n'
        if components['pm10'] != '':
            message += "PM10: " + str(components['pm10']) + '\n'
        if components['nh3'] != '':
            message += "NH3: " + str(components['nh3']) + '\n'

    return message


def search_city(name): 
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={name}&appid={API_KEY}"
    resp = requests.get(url)
    res = []
    if resp.status_code == 200:
        data = json.loads(resp.text)
        for d in data:
            res.append({'name': d['name'], 'lat': d['lat'], 'lon': d['lon']})
    return res


def city_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}"
    
    resp = requests.get(url)
    if resp.status_code == 200:
        data = json.loads(resp.text)
        weather = data['weather'][0]['description']
        main = data['main']
        country = data['sys']['country']
        sunrise = convert_date(int(data['sys']['sunrise']))
        sunset = convert_date(int(data['sys']['sunset']))
        message = ""
        message += "Country: " + country + '\n'
        message += "Sunrise: " + sunrise + '\n'
        message += "Sunset: " + sunset + '\n'
        message += "Weather: " + weather + '\n'
        message += "Temperature: " + str(main['temp']) + '\n'
        message += "Feels Like: " + str(main['feels_like']) + '\n'
        message += "Minimum Temperature: " + str(main['temp_min']) + '\n'
        message += "Maximum Temperature: " + str(main['temp_max']) + '\n'
        message += "Pressure: " + str(main['pressure']) + '\n'
        message += "Humidity: " + str(main['humidity']) + '\n'
        return message
    
    return "Nothing Found!"
        
def full_data(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}"
    resp = requests.get(url)
    
    if resp.status_code == 200:
        data = json.loads(resp.text)
        try:
            if data['cod'] == "200":
                message = ""
                data = data['list']
                l = len(data)
                for i in range(min(5, l)):
                    d = data[i]
                    message += "Date and Time:" + convert_date(int(d['dt'])) + "\n"
                    main = d['main']
                    weather = d['weather'][0]['description']
                    message += "Weather: " + weather + '\n'
                    message += "Temperature: " + str(main['temp']) + '\n'
                    message += "Feels Like: " + str(main['feels_like']) + '\n'
                    message += "Minimum Temperature: " + str(main['temp_min']) + '\n'
                    message += "Maximum Temperature: " + str(main['temp_max']) + '\n'
                    message += "Pressure: " + str(main['pressure']) + '\n'
                    message += "Humidity: " + str(main['humidity']) + '\n'
                    message += '-\n'
                return message
        except:
            pass
        
    return "Nothing Found!"

def fast_search(name): # ok
    url = f"https://api.codebazan.ir/weather/?city={name}"
    
    resp = requests.get(url)
    
    if resp.status_code == 200:
        data = json.loads(resp.text)
        try:
            if data['cod'] == "200":
                message = ""
                data = data['list']
                l = len(data)
                for i in range(min(4, l)):
                    d = data[i]
                    message += "Date and Time:" + convert_date(int(d['dt'])) + "\n"
                    main = d['main']
                    weather = d['weather'][0]['description']
                    message += "Weather: " + weather + '\n'
                    message += "Temperature: " + str(main['temp']) + '\n'
                    message += "Feels Like: " + str(main['feels_like']) + '\n'
                    message += "Minimum Temperature: " + str(main['temp_min']) + '\n'
                    message += "Maximum Temperature: " + str(main['temp_max']) + '\n'
                    message += "Pressure: " + str(main['pressure']) + '\n'
                    message += "Humidity: " + str(main['humidity']) + '\n'
                    message += '-\n'
                return message
        except:
            pass
        
    return "Nothing Found!"

def convert_date(dt):
    dt_utc_aware = datetime.datetime.fromtimestamp(
        dt, 
        datetime.timezone.utc).__str__()
    
    return dt_utc_aware

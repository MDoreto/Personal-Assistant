from datetime import datetime
import requests
from bs4 import BeautifulSoup

requests.packages.urllib3.disable_warnings()


class Services:
    def google_search(query):
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            'referer': 'https://www.google.com/'

        }
        url = 'https://www.google.com/search?q=' + query
        req = requests.get(url, headers=header, verify=False)
        soup = BeautifulSoup(req.text,'html.parser')
        a = soup.select_one('.Z0LcW')
        if a:
            return a.text
        a = soup.select_one('.ILfuVd')
        if a:
            return a.text
        return 'Não encontrei nada.'

    def consult_weather(parameters):
        if parameters['location']:
            city = parameters['location']['city']
        else:
            city = 'Diadema'
        api_key = 'ad1fe135975dfc854a7d44ad5eb67c2c'
        coord = {'Diadema': {'lat': -23.6861, 'lon': -46.6228},
                 'Santo André': {"lon": -46.5383, "lat": -23.6639}}
        if city in coord:
            lat = coord[city]['lat']
            lon = coord[city]['lon']
        else:
            response = requests.get(
                'https://api.openweathermap.org/data/2.5/weather', params={'appid': api_key, 'q': city}).json()
            if response['cod'] == '404':
                return 'Não consegui encontrar este local'
            lat = response['coord']['lat']
            lon = response['coord']['lon']
        query = {'lat': lat, 'lon': lon, 'units': 'metric',
                 'lang': 'pt_br', 'appid': api_key, 'exclude': 'minutely'}
        api_addres = 'https://api.openweathermap.org/data/2.5/onecall'
        response = requests.get(api_addres, params=query).json()
        if parameters['date-time']:
            if 'date_time' in parameters['date-time']:
                date = datetime.strptime(
                    parameters['date-time']['date_time'].split(':')[0], "%Y-%m-%dT%H")
                for data in response['hourly']:
                    if datetime.fromtimestamp(data['dt']) == date:
                        return get_weather_response(parameters, data)
            else:
                date = datetime.strptime(
                    parameters['date-time'].split('T')[0], "%Y-%m-%d")
                for data in response['daily']:
                    if datetime.fromtimestamp(data['dt']).date() == date.date():
                        return get_weather_response(parameters, data)
        else:
            data = response['current']
            return get_weather_response(parameters, data)
        return "Informação não encontrada"


def get_weather_response(parameters, i):
    if parameters['weather_type'] == 'pressure':
        return str(i['pressure'] / 1000) + ' bar'
    if parameters['weather_type'] == 'humidity':
        return str(i['humidity']) + '%'
    if parameters['weather_type'] == 'rain':
        return 'A probabilidade de chuva é de ' + str(i['pop']*100) + '%'
    temp = i['temp']
    if isinstance(temp, dict):
        return 'máxima de ' + str(temp['max']) + ' graus e mínima de ' + str(temp['min']) + ' graus, ' + i['weather'][0]['description']
    return str(temp) + ' graus, ' + i['weather'][0]['description']

#print(Services.google_search("qual a religiao predominante na russia"))

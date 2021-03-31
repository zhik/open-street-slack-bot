import requests
import datetime

class Weather():
    def __init__(self, latlng):
        forecastHourlyUrl = requests.get(f'https://api.weather.gov/points/{latlng}').json()['properties']['forecastHourly']
        self.forecast = requests.get(forecastHourlyUrl).json()
        self.periods = self.forecast['properties']['periods']


    def getForcast(self, dt):
        #match dt with a period and return string
        match = None
        for period in self.periods:
            t = datetime.datetime.fromisoformat(period['startTime']).replace(tzinfo=None)
            if t == dt:
                match = period

        if match:
            return f"{match['temperature']}F. {match['shortForecast']} ({match['windSpeed']})"
        else: 
            return '<https://www.wunderground.com/hourly/us/ny/new-york-city/KNYNEWYO806|forcast>'


def main():
    weather = Weather('40.7459,-73.9239')
    night = datetime.datetime.combine(datetime.date.today(), datetime.time(20, 0))
    weatherNight = weather.getForcast(night)
    print(weatherNight)

if __name__ == "__main__":
    main()
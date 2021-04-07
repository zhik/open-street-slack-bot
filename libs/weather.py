import requests
import datetime

class Weather():
    def __init__(self, latlng):
        forecastUrls = requests.get(f'https://api.weather.gov/points/{latlng}').json()['properties']
        
        try:
            self.dailyForecast = requests.get(forecastUrls['forecast']).json()
            self.dailyPeriods = self.dailyForecast['properties']['periods']
        except:
            self.dailyPeriods = []

        try:
            self.hourlyForecast = requests.get(forecastUrls['forecastHourly']).json()
            self.hourlyPeriods = self.hourlyForecast['properties']['periods']
        except:
            self.hourlyPeriods = []


    def getSummary(self, date):
        matches = []
        for period in self.dailyPeriods:
            d = datetime.datetime.fromisoformat(period['startTime']).replace(tzinfo=None).date()
            if d == date:
                matches.append(period)
        
        if matches:
            return '\n'.join([f"{match['name']}: {match['detailedForecast']}" for match in matches])
        else:
            return ''
        
    def getForecast(self, dt):
        #match dt with a period and return string
        match = None
        for period in self.hourlyPeriods:
            t = datetime.datetime.fromisoformat(period['startTime']).replace(tzinfo=None)
            if t == dt:
                match = period
                break

        if match:
            return f"{match['temperature']}F. {match['shortForecast']} ({match['windSpeed']})"
        else: 
            return '<https://www.wunderground.com/hourly/us/ny/new-york-city/KNYNEWYO806|forecast here>'


def main():
    weather = Weather('40.7459,-73.9239')
    night = datetime.datetime.combine(datetime.date.today(), datetime.time(20, 0))
    weatherNight = weather.getForecast(night)
    print(weatherNight)

    summary = weather.getSummary(datetime.date.today())
    print(summary) 

if __name__ == "__main__":
    main()
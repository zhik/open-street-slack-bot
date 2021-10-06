import requests
import datetime
from pytz import timezone

class SunriseSunset():
    def __init__(self, lat, lng):
        url = f'https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date=today&formatted=0'
        self.sunriseString = ''
        self.sunsetString = '' 

        print(url)

        data = requests.get(url).json()['results']
        
        try:

            #convert from datetime utc to nyc time
            sunrise = datetime.datetime.fromisoformat(data['sunrise']).replace(tzinfo=datetime.timezone.utc)
            sunset =  datetime.datetime.fromisoformat(data['sunset']).replace(tzinfo=datetime.timezone.utc)
            self.sunriseString = sunrise.astimezone(timezone('America/New_York')).strftime('%I:%M %p')
            self.sunsetString = sunset.astimezone(timezone('America/New_York')).strftime('%I:%M %p')

        except:
            print('ERROR')


def main():
    sunriseSunset = SunriseSunset(40.7459,-73.9239)

    print(sunriseSunset.sunriseString)
    print(sunriseSunset.sunsetString)

if __name__ == "__main__":
    main()
from libs.weather import Weather
import os
import datetime
import csv
import requests
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import time
load_dotenv()

#set timezone to eastern
os.environ['TZ'] = 'US/Eastern'
time.tzset()

def getBuddiesFromSheets(today):
    CSV_URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRm7akE9u9jQhN6XnmkRdwPwwrmd7PDXDdMRQ292H55UdE9DX-3LrLwLt4lyRxWcdjWHM5fZSPUtinv/pub?gid=1167005596&single=true&output=csv'
    signup39thDay = None
    signup39thNight = None
    signupSkillmanDay = None
    signupSkillmanNight = None

    with requests.Session() as s:
        download = s.get(CSV_URL)

        decoded_content = download.content.decode('utf-8')

        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        for row in my_list:
            date = row[1] + row[2]
            if date == today.strftime("%-m/%-d"):
                signup39thDay = ', '.join(i for i in row[3:5] if i)
                signup39thNight = ', '.join(i for i in row[5:7] if i)
                signupSkillmanDay = ', '.join(i for i in row[8:10] if i)
                signupSkillmanNight = ', '.join(i for i in row[10:] if i)
                break

    defaultRequest = '`Help!`'
    return {
        '39th-day': f'*{signup39thDay}*' if signup39thDay else '`39 Av 24/7`',
        '39th-night': f'*{signup39thNight}*' if signup39thNight else '`39 Av 24/7`',
        'skillman-day': f'*{signupSkillmanDay}*' if signupSkillmanDay else defaultRequest,
        'skillman-night': f'*{signupSkillmanNight}*' if signupSkillmanNight else defaultRequest
    }


def post(client, defaultChannel, date, now):
    # init weather
    weather = Weather('40.7459,-73.9239')

   # init time 
    now = datetime.datetime.now()
    currentUpdateTime = now.strftime('%-m/%-d %-I%p')

    # get signup and weather variables
    signup = getBuddiesFromSheets(date)

    day = datetime.datetime.combine(date, datetime.time(8, 0))
    night = datetime.datetime.combine(date, datetime.time(20, 0))
    weatherDay = weather.getForecast(day)
    weatherNight = weather.getForecast(night)
    weatherSummary = weather.getSummary(date)

    # check of cancellation
    typesOfCancellation = ('snow', 'wind', 'rain', 'storm')
    if any([i == signup['39th-day'].lower() or f'*{i}*' == signup['39th-day'].lower() for i in typesOfCancellation]):
        # build message
        message = {
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"Good evening! Barriers are on hold for *tomorrow ({date.strftime('%a %-m/%-d')})* due to `{signup['39th-day'].split(',')[0]}`."
                    }
                },
                {
                    'type': 'context',
                    'elements': [{
                        'type': 'mrkdwn',
                        'text':  weatherSummary
                    }]
                },
                {
                    'type': 'context',
                    'elements': [{
                        'type': 'mrkdwn',
                        'text': f"*UPDATE SCHEDULE <https://docs.google.com/spreadsheets/d/1-F81Ccr0jJxCaKKsttvSRBJyvmar08G2Q1YGomY1AeU/edit?usp=sharing|HERE>*. Post last updated on {currentUpdateTime}"
                    }]
                }
            ],
            'attachments': [
                {
                    "color": "#ffa700",
                    "blocks": [
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f"*8AM* - {date.strftime('%a %-m/%-d')}"
                            }
                        },
                        {
                            'type': 'context',
                            'elements': [{
                                'type': 'mrkdwn',
                                'text': weatherDay
                            }]
                        }
                    ]
                },
                {
                    "color": "#1919A3",
                    "blocks": [
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': "*8PM*"
                            }
                        },
                        {
                            'type': 'context',
                            'elements': [{
                                'type': 'mrkdwn',
                                'text': weatherNight
                            }]
                        }
                    ]
                }
            ]
        }
    else:
        message = {
            'blocks': [
                {
                    'type': 'section',
                    'text': {
                        'type': 'mrkdwn',
                        'text': f"Good evening! The weather and barrier budd(ies) for *tommorow ({date.strftime('%a %-m/%-d')})* are:"
                    }
                },
                {
                    'type': 'context',
                    'elements': [{
                        'type': 'mrkdwn',
                        'text':  weatherSummary
                    }]
                },
                {
                    'type': 'context',
                    'elements': [{
                        'type': 'mrkdwn',
                        'text': f"*UPDATE SCHEDULE <https://docs.google.com/spreadsheets/d/1-F81Ccr0jJxCaKKsttvSRBJyvmar08G2Q1YGomY1AeU/edit?usp=sharing|HERE>*. Post last updated on {currentUpdateTime}"
                    }]
                }
            ],
            'attachments': [
                {
                    "color": "#ffa700",
                    "blocks": [
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f"*8AM* - {date.strftime('%a %-m/%-d')}"
                            }
                        },
                        {
                            'type': 'context',
                            'elements': [{
                                'type': 'mrkdwn',
                                'text': weatherDay
                            }]
                        },
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f":three::nine:th Ave: {signup['39th-day']}"
                            }
                        },
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f":deciduous_tree: Skillman Ave: {signup['skillman-day']}"
                            }
                        }
                    ]
                },
                {
                    "color": "#1919A3",
                    "blocks": [
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': "*8PM*"
                            }
                        },
                        {
                            'type': 'context',
                            'elements': [{
                                'type': 'mrkdwn',
                                'text': weatherNight
                            }]
                        },
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f":three::nine:th Ave: {signup['39th-night']}"
                            }
                        },
                        {
                            'type': 'section',
                            'text': {
                                'type': 'mrkdwn',
                                'text': f":deciduous_tree: Skillman Ave: {signup['skillman-night']}"
                            }
                        }
                    ]
                }
            ]
        }

    print(message)
    #check `ts.text` to see if message has to be updated or new post is needed
    response = None
    try:
        with open('ts.txt', 'r') as file:
            lines = file.readlines()
            ts = lines[0].strip()
            channel = lines[1].strip()
    except:
        ts = None
        channel = None


    if channel is not None and now.hour != 18:
        #update
        response = client.chat_update(
            channel=channel,
            ts=ts,
            text=message['blocks'][0]['text']['text'],
            blocks = message['blocks'],
            attachments= message['attachments']
        )
    else:
        #post new
        try:
            response = client.chat_postMessage(
                channel=defaultChannel,
                text=message['blocks'][0]['text']['text'],
                blocks = message['blocks'],
                attachments= message['attachments']
                
            )
        except SlackApiError as e:
            # You will get a SlackApiError if "ok" is False
            assert e.response["error"]    # str like 'invalid_auth', 'channel_not_found'

    #save ts and currentUpdateTime
    ts=response.data['ts']
    channel = response.data['channel']
    print(ts)
    
    with open('ts.txt', 'w') as file:
        file.write(ts)
        file.write('\n')
        file.write(channel)

def main():
    #init slack client 
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    client = WebClient(token=slack_token)
    channel="#barrier-schedule"

    # get datetime
    today = datetime.date.today()
    now = datetime.datetime.now()
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)

    #do not run between the hours of 11pm - 5am
    if now.hour >= 23 or now.hour <= 5:
        return 0

    # if time is after 6pm post for tomorrow
    if now.hour >= 18:
        post(client, channel, tomorrow, now)
    else:
        post(client, channel, today, now)

if __name__ == "__main__":
    main()
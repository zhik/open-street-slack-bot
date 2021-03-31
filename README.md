# Slack bot for [Sunnyside Woodside Open Streets](https://twitter.com/SWOpenStreets)

### Setup

Setup python env

```bash
pip install virtualenv
virtualenv osbot-env
source ./osbot-env/bin/activate

pip install slack-sdk
pip install requests
pip install python-dotenv
```

Copy .env and replace with your slack token and secret.
```bash
cp .env.example .env
```

Run
```bash
python bot.py
```

### How does it work?

A cron job runs every hour. If the time is after 6pm the post if made with tomorrow's signups and weather.

If `snow`, `wind`, `rain`, or `storm` is in the first column 39th street morning signup a cancellation message is created, otherwise a normal one will be created.

See the [Slack bot kit website](https://api.slack.com/block-kit) on format/customz of the messages.

Lastly the existence of `ts.txt` is checked. This file contains information about time and id of the previous post. If it exist and it isn't 6pm, the previous message will be updated. Otherwise a new message will be created (at 6pm).

### Tips

- Delete `ts.txt` if you would like to post a new message
- You can change the channel in the main function, defaulted to "#bot-testing"
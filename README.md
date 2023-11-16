## Intro
This repository has all the tools needed for having a BOT that will transform any youtube video you send to the bot into a mp3 file.

Sadly, mp3 files from Telegram cannot be downloaded directly to your device for now.(convert_mp3_buffer function).

So if we want a bot that downloads mp3 files from youtube we will need to download the mp3 file and locally and serve that file.



## Installation and running

1. Set your Telegram `BOT_TOKEN` in your dotenv file
2. If you plan to serve files, set the `SERVER_URL` in your dotenv file
3. Install the dependencies and run the app for the first time.

```python3
pip3 install pipenv # if you don't have pipenv
pipenv install      # This will install the deps from the Pipfile
python3 main.py     # Run the app
```

4. Send a message to your bot containing a youtube URL. You'll get a music back

## Future TODOS
- Allow multiple youtube urls (from phone, etc.)
- Allow multiple sources (soundcloud? Spotify?)
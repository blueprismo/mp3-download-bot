## Intro
This repository has all the tools needed for having a BOT that will transform any youtube video you send to the bot into a mp3 file.
Sadly, mp3 files from Telegram cannot be downloaded directly to your device for now. But it's a nice demonstration

## Installation and running
1. Check out the respository
2. `pip install` should install all the dependencies
3. update your BOT_TOKEN in the `.env` file in the root of your repo
4. `python3 main.py`


## Future TODOS
- Allow mp3 files being downloaded (set up a server + storage) from a link served with fastAPI
- Allow multiple sources (soundcloud? Spotify?)
# Archive Bot

A very simple telegram bot that allows compression of multiple files into a ZIP archive



## Deploy to Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/mkasajim/tg_zip_bot)


## Deploy locally


Clone the repository:

```
git clone https://github.com/mkasajim/tg_zip_bot.git
```

Install requirements

```
pip3 install -r requirements.txt
```
Replace  
```
YOUR_BOT_TOKEN_HERE
``` 
with your bot token in the main.py file

Run the bot
```
python3 main.py
```

Command list
```
start - Start the bot
zip - Start the zipping process. The bot will now accept files to be zipped.
stopzip - Stop the zipping process, zip the received files, and send the zipped file back to the user.
```

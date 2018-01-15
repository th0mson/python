# WebMon

Bot for monitoring web sites



For install need^
1. sudo apt-get update && sudo apt-get install python python-pip
2. sudo pip install requests
3. Edit the config file: config.json
   - Set your Telegram bot token in to param "tg_bot_token";
   - Set your Telegram chanel/chat id in to param "tg_shanel_id";
   - Set URL's for monitoring in to param "check_url";
   - Set word/string to parsing in your sites in to param "check_str";


For testing run:

python webcheck.py

If all right you ara get the test message

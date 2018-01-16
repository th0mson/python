# WebMon

Bot for monitoring web sites

Install:
1. sudo apt-get update && sudo apt-get install python python-pip
2. sudo pip install requests
3. Clone repository to your local script folder

Configuration:

Edit the config file: config.json
   - Set your Telegram bot token in to param "tg_bot_token";
   - Set your Telegram chanel/chat id in to param "tg_shanel_id";
   - Set URL's for monitoring in to param "check_url";
   - Set word/string to parsing in your sites in to param "check_str";
   - Edit timeout (sec) for webCheckDaemon in to param daemon_timeout;
   - Edit timeout (sec) for tg_bot timeout in to param tg_bot_timeout;

For testing run in script path:

python tgbot.py
python webcheck.py

if all right, you are get Test messages


For run full monitoring, you are need starting Daemon:

python <Script_Path>/webcheckdaemon.py start

Add this command to /etc/rc.local to start this daemon in start your OS

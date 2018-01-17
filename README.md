# WebMon

Bot for monitoring web sites

## Installing:
1. ```sudo apt-get update && sudo apt-get install python python-pip```
2. ```sudo pip install requests```
3. ```Clone repository to your local script folder```

## Configuration:
Edit the config file: config.json
   - Set your Telegram bot token in to param "tg_bot_token";
   - Set your Telegram chanel/chat id in to param "tg_shanel_id";
   - Set URL's for monitoring in to param "check_url";
   - Set word/string to parsing in your sites in to param "check_str";
   - Edit timeout (sec) for webCheckDaemon in to param daemon_timeout;
   - Edit timeout (sec) for tg_bot timeout in to param tg_bot_timeout;

## Testing:
For testing run scripts in your script folder:

```python tgbot.py```

```python webcheck.py```

if all right, you are get Test messages to your Telegram Chanel/Chat

## Start:
### For run full monitoring, you are need starting Daemon:

```python <Script_Path>/webcheckdaemon.py start```

## SYSTEMD:
- Set path to script in to param "WorkingDirectory" ```webmon.service```
- Copy ```webmon.service``` to ```/etc/systemd/system/webmon.service```
- run Daemon with command:

  ```systemctl start webmon.service```

- for autorun service - execute:

  ```systemctl enable webmon.service```

## Ansible:
- Edit ansible playbook ```webmon.yml``` vars param:
  - Set local project path where will install scripts in param ```project_location```;
  - Set in ```tg_bot```:
    - Set tg_bot_token in ```value``` key;
    - Set tg_chanel_id in ```value``` key;
  - Set in ```ls_sites```:
    - Set key name in ```key```;
    - Set url and string/word in param ```value``` for keys ```check_url``` and ```check_str```;
- Run:

  ```ansible-playbook webmon.yml```
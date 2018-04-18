#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, logging, tempfile
import json
import requests #pip install requests

from datetime import timedelta, datetime
from tgbot import TG_Bot

class WebCheck:
    # default timeout
    daemonTimeoutDefault = 1 #sec
    tgBotTimeoutDefault  = timedelta(seconds=60) #sec
    lastCheckTime = {}

    def __init__(self):
        # Log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/' + (os.path.basename(__file__)).split('.')[0] + '.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s %(levelname)s: %(message)s',
                            datefmt = '%Y-%m-%d %I:%M:%S')
        logging.info('Daemon start')

        # Read config
        cfgPath = os.path.dirname(os.path.realpath(__file__)) + '/config.json'

        if os.path.exists(cfgPath):
            with open(cfgPath) as json_data_file:
                cfg = json.load(json_data_file)
        else:
            self.fireNotify('File "config.json" does not exist. Daemon stopped.')
            sys.exit(2)

        # -- Main parameters
        ## Load Telegram Params:
        if 'tg_bot' not in cfg:
            message = 'Is not define Telegram Bot params (tg_bot) in "config.json". Daemon stopped.'
            self.fireNotify(message)
            logging.error(message)
            sys.exit(2)

        if 'tg_bot_token' in cfg['tg_bot']:
            self.tgbot_token = cfg['tg_bot']['tg_bot_token']
        else:
            message = 'Is not define Telegram Bot Token params (tg_bot_token) in "config.json". Daemon stopped.'
            self.fireNotify(message)
            logging.error(message)
            sys.exit(2)

        if 'tg_chanel_id' in cfg['tg_bot']:
            self.tgbot_chanel_id = cfg['tg_bot']['tg_chanel_id']
        else:
            message = 'Is not define Telegram Bot Chat ID params (tg_chanel_id) in "config.json". Daemon stopped.'
            self.fireNotify(message)
            logging.error(message)
            sys.exit(2)

        if 'tg_proxy_socks_host' in cfg['tg_bot']:
            self.tgbot_proxy_socks_host = cfg['tg_bot']['tg_proxy_socks_host']
        else:
            self.tgbot_proxy_socks_host = ""

        if 'tg_proxy_socks_port' in cfg['tg_bot']:
            self.tgbot_proxy_socks_port = cfg['tg_bot']['tg_proxy_socks_port']
        else:
            self.tgbot_proxy_socks_port = ""

        if self.tgbot_proxy_socks_host != "":
#            self.tgbot_proxy_socks = "socks5://{}:{}".format(self.tgbot_proxy_socks_host, self.tgbot_proxy_socks_port)
            self.tgbot_proxy_socks = "{}:{}".format(self.tgbot_proxy_socks_host, self.tgbot_proxy_socks_port)
        else:
            self.tgbot_proxy_socks = ""

        ## Load Site list
        if 'list_sites' not in cfg:
            message = 'Is not define Sites List params (sites_list) in "config.json". Daemon stopped.'
            self.fireNotify(message)
            logging.error(message)
            sys.exit(2)
        else:
            self.ListSites = cfg['list_sites']

        ## Set daemon timeout
        if 'daemon_timeout' in cfg['main']:
            self.daemonTimeout = cfg['main']['daemon_timeout']
        else:
            self.daemonTimeout = self.daemonTimeoutDefault

        ## Set tg_bot timeout for error message
        if 'tg_bot_timeout' in cfg['main']:
            self.tgBotTimeout = timedelta(seconds=cfg['tg_bot']['tg_bot_timeout'])
        else:
            self.tgBotTimeout = self.tgBotTimeoutDefault

    def fireNotify(self, msg = ''):
        """
        Fire notify action
        """
        TGBot = TG_Bot(self.tgbot_token)
        TGBot.SendMessage(self.tgbot_proxy_socks, self.tgbot_chanel_id, msg)

        logging.info('Called fireNotify()')

    def getDaemonTimeout(self):
        """
        Get daemon checking timeout
        """
        return self.daemonTimeout

    def getTgBotTimeout(self):
        """
        Get tg bot error message timeout
        """
        return self.tgBotTimeout

    def webParser(self, check_data, search_str):
        """
        Search word/string in resurse
        """
        c = 0
        if search_str in check_data.decode('utf-8'):
            c += 1
        else:
            c = 0
        return c

    def check(self, lastCheckTime = None, testStatus = None):
        """
        Checking sources
        """
        logging.info('Called check()')

        ## Checking all site in List from config
        for site in sorted(self.ListSites):
            logging.debug('sourceCheck: %s', self.ListSites[site]['check_url'])
            parser_count = 0

            try:
                ## Get request
                response = requests.get(self.ListSites[site]['check_url'])
                ## Search word/string in get request
                parser_count = self.webParser(response.content, self.ListSites[site]['check_str'])
            except requests.exceptions.ReadTimeout:
               print('Oops. Read timeout occured')
            except requests.exceptions.ConnectTimeout:
               print('Oops. Connection timeout occured!')
            except requests.exceptions.ConnectionError:
               print('Seems like dns lookup failed..')
            except requests.exceptions.HTTPError as err:
               print('Oops. HTTP Error occured')
               print('Response is: {content}'.format(content=err.response.content))

            # testing
            if testStatus == 'test':
                self.fireNotify('Hostname: {}\nService: WEBCHECK\nStatus: INFO\nMSG:\nTesting config:\nURL = {},\nword/string = {}'.format(os.uname()[1], self.ListSites[site]['check_url'], self.ListSites[site]['check_str']))

            # If word/string not found in get request or site not loaded then send message to telegram
            if parser_count == 0:
                CurrentCheckTime = datetime.now()
                message = 'Hostname: {}\nService: WEBCHECK\nStatus: WARNING\nMSG: {} is broken {} not found'.format(os.uname()[1], self.ListSites[site]['check_url'], self.ListSites[site]['check_str'])
                if (site not in self.lastCheckTime):
                    self.lastCheckTime[site] = datetime.now()
                    self.fireNotify(message)

                # send message to telegram with interval from tgBotTimeout variable
                if ((CurrentCheckTime - self.tgBotTimeout) >= self.lastCheckTime[site]):
                    self.fireNotify(message)
                    self.lastCheckTime[site] = CurrentCheckTime

        logging.info('End check()')
        return self

if __name__ == '__main__':
    c = WebCheck()
    c.check(testStatus = 'test')

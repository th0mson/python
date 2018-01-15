#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, subprocess, logging, tempfile
import json

from datetime import datetime
from tgbot import TG_Bot

class WebCheck:
    """
    A generic webcheck class.

    """

    # default timeout for demon
    daemonTimeoutDefault       = 10 #sec

    def __init__(self):
        # log init
        logging.basicConfig(filename = tempfile.gettempdir() + '/' + __file__.split(".")[-1] + '.log',
                            level = logging.DEBUG,
                            format = '%(asctime)s %(levelname)s: %(message)s',
                            datefmt = '%Y-%m-%d %I:%M:%S')
        logging.info('Daemon start')

        # read config
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

        ## Load Sites list
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

        ## First message for start Daemon
        self.fireNotify('Monitoring up')

    def fireNotify(self, msg = ''):
        """
        Fire notify action
        """

        TGBot = TG_Bot(self.tgbot_token)
        TGBot.SendMessage(self.tgbot_chanel_id, msg)

        logging.info('Called fireNotify()')

    def getLastCheckTime(self):
        """
        To simplicity, time of last modification of the current file is used as the time of last checking
        """
        lastCheckTime = os.path.getmtime(__file__)
        return datetime.fromtimestamp(lastCheckTime)

    def setLastCheckTime(self, time = None):
        """
        Set time of last checking -> touch file
        """
        #commands.getoutput('touch ' + __file__)
        #os.system('touch ' + __file__)
        subprocess.check_output('touch ' + __file__, shell=True)
        return self

    def getDaemonTimeout(self):
        """
        Get daemon checking timeout
        """
        return self.daemonTimeout

    def check(self, lastCheckTime = None, repositoryPath = None):
        """
        Get log as string
        """
        logging.info('Called check()')
        if (not lastCheckTime):
            lastCheckTime = self.getLastCheckTime()


#        for item in self.ListSites:
#            logging.debug('sourceOutput: %s', sourceOutput)
#            parser = webParser.webParser(sourceOutput)
#            strStatus = parser.getSTRStatus()

        self.setLastCheckTime()

#       self.fireNotify('Test Message {}'.format(lastCheckTime))

        logging.info('End check()')
        return self

if __name__ == '__main__':
    c = WebCheck()
    c.check()

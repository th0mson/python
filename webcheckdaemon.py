#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, time, tempfile
import daemon, webcheck
 
class WebCheck(daemon.Daemon):
    def run(self):
        c = webcheck.WebCheck()

        # First message for start Daemon
        c.fireNotify('Hostname: {}%0AService: WEBCHECK%0AStatus: INFO%0AMSG: Monitoring up'.format(os.uname()[1]))

        while True:
            c.check()
            time.sleep(c.getDaemonTimeout())

    def stop(self):
        # Message for stop Daemon
         webcheck.WebCheck().fireNotify('Hostname: {}%0AService: WEBCHECK%0AStatus: INFO%0AMSG: Monitoring Down'.format(os.uname()[1]))

if __name__ == '__main__':
    pidFile = tempfile.gettempdir() + '/webmon.pid'
    daemon = WebCheck(pidFile)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            print 'Daemon starting..'
            daemon.start()
            print 'Daemon started!'
        elif 'stop' == sys.argv[1]:
            print 'Daemon stopping..'
            daemon.stop()
            print 'Daemon stopped!'
        elif 'restart' == sys.argv[1]:
            print 'Daemon restarting..'
            daemon.restart()
            print 'Daemon restarted!'
        else:
            print 'Unknown command'
            sys.exit(2)
        sys.exit(0)
    else:
        print 'usage: %s start|stop|restart' % sys.argv[0]
        sys.exit(2)

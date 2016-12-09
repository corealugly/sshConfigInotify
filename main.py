from daemon import daemon
import sys, time, os

import logging
import inotify.adapters

import fnmatch


# from func import createConfigUserV2
import func
import pwd,sys, configparser

from func import sshConfigInotify


class MyDaemon(daemon):
    def run(self):
        print('config:' + self.config)
        inotify = sshConfigInotify(self.config)
        inotify.inotify_watcher()
        # i = inotify.adapters.Inotify()
        # username = os.uname()
        # homename = os.environ['HOME']
        #
        # fullpath = b'/home/' + username + b'/.ssh/'
        # pattern = re.compile('config_\w*$')
        # i.add_watch(fullpath)
        # try:
        #     for event in i.event_gen():
        #         if event is not None:
        #             (header, type_names, watch_path, filename) = event
        #             print("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
        #                          "WATCH-PATH=[%s] FILENAME=[%s]",
        #                          header.wd, header.mask, header.cookie, header.len, type_names,
        #                          watch_path.decode('utf-8'), filename.decode('utf-8'));
        #             if type_names[0] == 'IN_MODIFY' and pattern.match(filename.decode('utf-8')):
        #                 createConfig(username.decode('utf-8'))
        # finally:
        #     i.remove_watch(fullpath)

if __name__ == "__main__":
    pidfile = '/tmp/ssh_watcher.pid'
    logfile = '/tmp/ssh_watcher.log'
    configfile  = '/etc/default/ssh_watcher.conf'

    daemon = MyDaemon(pidfile, logfile, logfile, configfile)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)
from daemon import daemon
import sys, time, os

import logging
import inotify.adapters

import glob
import fnmatch
import re

def createConfig(username):
    with open('/etc/passwd', 'r') as ps:
        for line in ps:
            if username in line:
                global home_dir
                home_dir = line.split(':')[5]
                break
    config_list = glob.glob(home_dir + '/.ssh/config_*')
    print(config_list)
    with open(home_dir + '/.ssh/config', 'w') as outfile:
        for filename in config_list:
            with open(filename, 'r') as infile:
                outfile.write(infile.read())

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


class MyDaemon(daemon):
    def run(self):
        i = inotify.adapters.Inotify()
        username = os.uname()
        homename = os.environ['HOME']

        fullpath = b'/home/' + username + b'/.ssh/'
        pattern = re.compile('config_\w*$')
        i.add_watch(fullpath)
        try:
            for event in i.event_gen():
                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    _LOGGER.info("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                                 "WATCH-PATH=[%s] FILENAME=[%s]",
                                 header.wd, header.mask, header.cookie, header.len, type_names,
                                 watch_path.decode('utf-8'), filename.decode('utf-8'))
                    print("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                                 "WATCH-PATH=[%s] FILENAME=[%s]",
                                 header.wd, header.mask, header.cookie, header.len, type_names,
                                 watch_path.decode('utf-8'), filename.decode('utf-8'))
                    if type_names[0] == 'IN_MODIFY' and pattern.match(filename.decode('utf-8'):
                        createConfig(username.decode('utf-8'))
        finally:
            i.remove_watch(fullpath)

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

# def main():
#     i = inotify.adapters.Inotify()
#     username = b'corealugly'
#     fullpath = b'/home/'+ username + b'/.ssh/'
#
#     i.add_watch(fullpath)
#     try:
#         for event in i.event_gen():
#             if event is not None:
#                 (header, type_names, watch_path, filename) = event
#                 _LOGGER.info("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
#                              "WATCH-PATH=[%s] FILENAME=[%s]",
#                              header.wd, header.mask, header.cookie, header.len, type_names,
#                              watch_path.decode('utf-8'), filename.decode('utf-8'))
                # if type_names[0] == 'IN_MODIFY':
                #     print(filename)
    # finally:
    #     i.remove_watch(fullpath)

# if __name__ == "__main__":
#     _configure_logging()
#     main()
import pwd,sys, configparser
import inotify.adapters
import re
import glob

def createConfigUser(username):
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

def createConfigUserV2(username):
    user_info = pwd.getpwnam(username)
    config_list = glob.glob(user_info.pw_dir + '/.ssh/config_*')
    with open(user_info.pw_dir + '/.ssh/config', 'w') as outfile:
        for filename in config_list:
            with open(filename, 'r') as infile:
                outfile.write(infile.read())

class sshConfigInotify:

    def __init__(self, config):
        print('inside:' + config)
        configPars = configparser.ConfigParser()
        configPars.read(config)
        self.username = configPars.get('ssh_watcher', 'username').split(',')
        self.config_path = config

    def inotify_watcher(self):
        i = inotify.adapters.Inotify()
        # username = os.uname()
        # homename = os.environ['HOME']

        for uname in self.username:
            user_info = pwd.getpwnam(uname)
            fullpath = user_info.pw_dir.encode('utf-8') + b'/.ssh/'
            print(b'full_path:' + fullpath)
            i.add_watch(fullpath)

        try:
            pattern = re.compile('config_\w*$')
            for event in i.event_gen():
                if event is not None:
                    (header, type_names, watch_path, filename) = event
                    print("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                                 "WATCH-PATH=[%s] FILENAME=[%s]",
                                 header.wd, header.mask, header.cookie, header.len, type_names,
                                 watch_path.decode('utf-8'), filename.decode('utf-8'));
                    if type_names[0] == 'IN_MODIFY' and pattern.match(filename.decode('utf-8')):
                        print('CREATE_CONFIG')
                        createConfigUserV2(watch_path.decode('utf-8').split('/')[2])
        finally:
            for uname in self.username:
                user_info = pwd.getpwnam(uname)
                fullpath = user_info.pw_dir.encode('utf-8') + b'/.ssh/'
                i.remove_watch(fullpath)
This program creates a configuration file ssh when changing config file format config_*
this code need activate from systemd unit.

unit_dir: /etc/systemd/system/

example unit.

[Unit]
Description=ssh_watcher

[Service]
Type=forking
PIDFile=/tmp/ssh_watcher.pid
User=root
Group=root
OOMScoreAdjust=-100

ExecStart=/usr/bin/python3 /home/corealugly/PycharmProjects/sshConfigInotify/main.py start
ExecStop=/usr/bin/python3 /home/corealugly/PycharmProjects/sshConfigInotify/main.py stop
ExecReload=/usr/bin/python3 /home/corealugly/PycharmProjects/sshConfigInotify/main.py restart


[Install]
WantedBy=multi-user.target
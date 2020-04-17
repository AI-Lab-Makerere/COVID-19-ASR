#### crontab entry to start the shell script at 6.am EA Time
0 3 * * * /usr/local/bin/ripper.sh >> /var/log/ripper.log 2>&1
#### crontab entry to stop streamripper befoe midnight
59 23 * * * /usr/bin/killall streamripper




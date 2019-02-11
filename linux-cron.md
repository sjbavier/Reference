# Basic cron utilization /etc/ #

List scheduled crontab commands

```sh
crontab -l
```

Edit crontab ( some systems will not allow users to create crontab entries unless their username is located in [/etc/cron.allow])

```sh
crontab -e
```

To run a script that executes at 5:47 in the morning each day, edit crontab

```sh
47 5  *  *  * /home/username/script.sh
```

Anacron is used to schedule automated operations when you cannot guarantee that a machine will be on always
Example [/etc/anacrontab]

```sh
1 5 cron.daily run-parts --report /etc/cron.daily # job executes any scripts in the /etc/cron.daily directory once a day 5 min after boot
7 10 cron.weekly run-parts --report /etc/cron.weekly # job executes any scripts in the /etc/cron.weekly directory onece a week 10 min after boot
```
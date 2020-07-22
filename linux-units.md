# Working with systemctl units

Systemd manages system services, devices, system timers and targets (systemd equivalent to runlevels).

Systemd objects are called **service units** and for each unit there is a unit file for configuration.

---

## Viewing systemd units

To list systemd unit files

```sh
# show enabled service units
systemctl list-unit-files -t service
# -a shows enabled and disabled service unit files
# output is unit file and STATE
systemctl list-unit-files -at service
```

List enabled units

```sh
# show enabled running services
systemctl list-units -t service
systemctl list-unit-files --type=service --state=enabled
# -a show enabled non-running services as well
systemctl list-units -at service
```

List services running

```sh
systemctl list-units -t service --state running
```

---

## Viewing service unit files

Examine a service

```sh
systemctl cat <service-name>
```

Example .service file

```console
example: systemctl cat gcs-sync

[Unit]
Description=C2D GCS Sync
[Service]
CPUQuota=50%
Type=simple
Restart=always
RestartSec=3
WorkingDirectory=/opt/c2d/downloads
ExecStart=/opt/c2d/downloads/gcs-sync
StandardOutput=journal
User=root
[Install]
WantedBy=multi-user.target
```

## Start, stop, status, enable and disable

Get the status of a service

```sh
systemctl status <service>
```

Stop a service

```sh
systemctl stop <service>
```

Force a service to load on system startup

```sh
systemctl enable <service>
```

Remove a service from system startup

```sh
systemctl disable <service>
```

Restart a service

```sh
systemctl restart <service>
```

---

## systemd timers

Alternative to cron jobs

- Real-Time timers
  - similar to cron jobs
  - activate on calendar events
- Monotonic timers
  - activate on time span relative to event

Benefits of timers rather than cron jobs

- each timer has its own service unit file
- can start independently of their timer
- can be configured to run in their own environment
- jobs can be attached to cgroups
- jobs can have dependencies on other systemd units
- jobs are logged in the systemd journal

Timers are named with a .timer extension with corresponding .service file

list timers

```sh
systemctl list-timers
```

Sample timer or .timer file

- OnCalendar creates a Real-Time calendar

```console
[Unit]
Description=System backup every day at 2AM

[Timer]
OnCalendar=*-*-* 02:00:00
Unit=<service>.service

[Install]
WantedBy=multi-user.target
```
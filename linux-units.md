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
# example: systemctl cat rsyslog
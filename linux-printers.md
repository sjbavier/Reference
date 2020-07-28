# Working with printer

Printers can be configured through localhost:631, though you may have to enable your group or **wheel** in the **etc/cups-files.conf**

Additional configuration can be found in **/etc/cups/cupsd.conf**

To get a list of print queues

```sh
lpstat -a
```

Check printers status

```sh
lpstat -p
lpstat -s
# you may have to restart cups
systemctl restart cups
```

See print jobs

```sh
lpq -a
```

To remove a print job from the queue

```sh
lprm <job-#>
```

Change print options while in queue

```sh
lp -i <job-#> -n <copies> -p <priority>
```

Move print job from one print queue to another

```sh
lpmove <printer-1> <printer-2>
```

To print text from file

```sh
lpr <file>
```
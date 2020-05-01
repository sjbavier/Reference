# Collection of snippets for archiving filesystems in linux

To display partitions currently mounted on a linux system **running df on lxc container shows only partitions associated with LXC host**

```sh
df -h # -h flag dictates a human readable byte format
```

To copy to a tar archive all files

```sh
tar cvf archive-name.tar * # c create v for verbose f file
```

To copy to a tar archive all files including hidden files beginning with .

```sh
tar cvf archive-name.tar .
```

For further compression add the z

```sh
tar czvf archive.tar.gz *.mp4 # compresses all .mp4 extension files
```

To split a tar archive into 1G chunks

```sh
split -b 1G archive.tar.gz "archive.tar.gz.part"
```

To recreate the 1G parts into a whole, use cat

```sh
cat archive.tar.gz.part* > archive.tar.gz
```

To extract a tar gzip archive

```sh
tar xzvf archive.tar.gz
```

To extract a tar

```sh
tar xvf archive.tar
```

To extract to another directory

```sh
tar -C <directory> -xzvf archive.tar.gz
tar -C <directory> -xvf archive.tar
```

To pipe an archive over ssh

```sh
tar czvf - --one-file-system / /usr /var \ # the - in czvf - outputs data to standard output pushing the details to the end of the command, --one-file-system argument excludes all data from any filesystem besides current and won't include pseudo partitions like /sys/ and /dev/
--exclude=/home/temp/ | ssh <user>@<host> \ # --exclude lets you exclude data from current file system
"cat > /home/backups/backup-file.tar.gz" # cat is executed against the archive data stream
```

Use find to search through file system objects

```sh
find /var/www/html -iname <1> "*.html" -exec tar \ # -iname returns both upper and lowercase ( -name for case-sensitive ) -exec is execute if true `0` status is returned until the ; is encountered the {} is replaced by the current file being processed
-rvf html.tar {} \; # -r flag is used to append rather than overwrite, the \; is used to escape to protect from expansion by the shell
```

Also can use locate

```sh
locate *.js
```

Locate searches a preexisting index (updated upon boot) to update

```sh
updatedb
```

To unzip .zip files use package unzip

```sh
unzip <file> -d <destination-directory>
```

To unzip .gz extensions use gzip/gunzip

```sh
gunzip <file>
gzip <file>
```
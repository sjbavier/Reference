# Working with find

find all files with extension

```sh
find . -type f -name "*.txt"
```

Find all files in a directory recursively and chmod 644

```sh
find <directory> -type f -exec chmod 644 {} \;
# -type f for regular file
# -exec for command to execute
```

Find all directories and change permission to 755

```sh
find <directory> -type d -exec chmod 755 {} \;
# -type d for regular directory
# -exec for command to execute
```

Find last modified files recursively

```sh
find <directory> -type f -print0 | xargs -0 stat --format '%Y :%y %n' | sort -nr | cut -d: -f2-
# -print0 - print full name on stdout followed by null instead of newline like -print
# -print0 works in conjunction with xargs -0
# xargs - build and execute command lines from stdin
# -0 input items are terminated by a null character, disables end of file string, useful when input items might contain whitespace quotes or backslashes
# stat - display file or file system status
# --format or -c - to modify default format
# sort -nr - sort numeric reverse
# cut - remove sections from each line of files
# cut -d: - the delimiter is ':'
# cut -f2 - second field
# cut -f2- - second field to end of line
```

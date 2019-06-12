# Working with find

find all files with extension

```sh
find . -type f -name "*.txt"
```

Find all files in a directory recursively and chmod 644

```sh
find <directory> -type f -exec chmod 644 {} \;
```

Find all directories and change permission to 755

```sh
find <directory> -type d -exec chmod 755 {} \;
```

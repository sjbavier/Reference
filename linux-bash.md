# Some samples of common scripts

Search a directory for any files with spaces and replace with underscores

```sh
#!/bin/bash
echo "which directory would you like to check?"
read directory
find $directory -type f | while read file; do
if [[ "$file" = *[[:space:]]* ]]; then
mv "$file" `echo $file | tr ' ' '_'`
fi;
done
```
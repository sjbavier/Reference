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

Change shell to zsh

```sh
chsh -s $(which zsh)
```

## Next sections from [https://gist.github.com/LeCoupa/122b12050f5fb267e75f] bash cheatsheet

## File Commands

```sh
ls                            # lists your files
ls -l                         # lists your files in 'long format', which contains the exact size of the file, who owns the file and who has the right to look at it, and when it was last modified
ls -a                         # lists all files, including hidden files
ln -s <filename> <link>       # creates symbolic link to file
touch <filename>              # creates or updates your file
cat > <filename>              # places standard input into file
more <filename>               # shows the first part of a file (move with space and type q to quit)
head <filename>               # outputs the first 10 lines of file
tail <filename>               # outputs the last 10 lines of file (useful with -f option)
emacs <filename>              # lets you create and edit a file
mv <filename1> <filename2>    # moves a file
cp <filename1> <filename2>    # copies a file
rm <filename>                 # removes a file
diff <filename1> <filename2>  # compares files, and shows where they differ
wc <filename>                 # tells you how many lines, words and characters there are in a file
chmod -options <filename>     # lets you change the read, write, and execute permissions on your files
gzip <filename>               # compresses files
gunzip <filename>             # uncompresses files compressed by gzip
gzcat <filename>              # lets you look at gzipped file without actually having to gunzip it
lpr <filename>                # print the file
lpq                           # check out the printer queue
lprm <jobnumber>              # remove something from the printer queue
genscript                     # converts plain text files into postscript for printing and gives you some options for formatting
dvips <filename>              # print .dvi files (i.e. files produced by LaTeX)
grep <pattern> <filenames>    # looks for the string in the files
grep -r <pattern> <dir>       # search recursively for pattern in directory
```

## Directory Commands

```sh
mkdir <dirname>  # makes a new directory
cd               # changes to home
cd <dirname>     # changes directory
pwd              # tells you where you currently are
```
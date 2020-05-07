# Working with streams

Streams are simply sequences of bytes that can be read or written.  The complexity is hidden by using library functions allowing interactions with terminals, files, network sockets and devices.

- **stdin** standard input stream: provides input to commands
- **stdout** standard output stream: displays output from commands
- **stderr** standard error: displays error output from commands

## Piping with |

Many text processing commands can take input either from a file or the standard input stream.

```sh
echo -e "egg\ncat\nbanana" | sort
banana
cat
egg
```

Hiphen - is often used to negate using a filename and default to stdin.

```sh
# listen on a port and tar the incoming data stream
nc -l -p 13003 | tar xvzf -
```

## Output redirection >

To save the output of a command use the > operator

```sh
ls -alt | grep "match" > fileoutput.txt
```

## cat, od and split

### cat or tac (reverse)

**cat** is short for concatenate, used to display the contents of a file on stdout

```sh
cat <file>
# filter and redirect to another file
cat <file> | grep <pattern> > <file2>

# cat multiple files together such as file1 file2 etc. file*
cat <file>*
```

### od (octal dump)

GNU text utilities come with **od**
Several options are available 
**-A** to control the --address-radix of the file offets ( o, (octal, the default), d (decimal), x (hexadecimal), or n (no offsets displayed) )
 **-t** to control the form of the displayed contents

```sh
od dogs.txt
# example output
# 0000000 067544 071547 005072 052011 062145 074544 005054 052011
# 0000020 061157 005151
# 0000024

# (-A d) decimal other options (o: octal, x: hex, n: none)
# (-t c ) type printable characters or backslash escapes
od -A d -t c dogs.txt
# example output
# 0000000   d   o   g   s   :  \n  \t   T   e   d   d   y   ,  \n  \t   T
# 0000016   o   b   i  \n
# 0000020

# (-A n) no offset (-t a) output type = select named characters ignore high-order bit
od -A n -t a dogs.txt
# example output
#    d   o   g   s   :  nl  ht   T   e   d   d   y   ,  nl  ht   T
#    o   b   i  nl
```

## split

Used to split files and arrange file name prefixes and suffixes, as well as delineate parameters for the split.

By default files resulting from split have an x, followed by a suffix of 'aa','ab', ... etc.

```sh
# split files containing at most 2 lines
split -l 2 <file>

# split files containing at most 18 bytes and supply a prefix of y
split -b 17 <file> y
```

## wc, head and tail

### wc

wc is used to display the number of lines, words and bytes in a file.

```sh
wc <file>
# examples output
# <lines> <word-count> <bytes> <file>
wc -l <file>
# example output
# <lines> <file>
```

### head

head is used for displaying the first part of a file or output, default is 10 lines

```sh
# top 10 disk usage not including size of subdirectories, reverse comparison, human readable
du -Sh | sort -rh | head
```

### tail

tail is used for displaying the end of a file or output, default is 10 lines

```sh
# last 10 lines of dmesg
dmesg | tail

# follow the file
tail -f /var/log/<log>
```

## expand, unexpand and tr

```sh
# swap tabs for spaces
expand -t 1 <file>

# swap spaces for tabs ( requires at least 2 spaces to convert )
unexpand -t 1 <file>

# translate spaces to tabs (tr is a pure filter)
cat <file> | tr ' ' '\t'
```

## pr, nl and fmt

pr command is used to format files for printing

nl command numbers lines ( can also use cat -n )

fmt is used to format text

```sh
# side by side file printing
pr -m <file1> <file2> 

# line numbes
nl <file>

# format file output to 60 characters wide
fmt -w 60 <file>
```

## sort and uniq

sort command sorts input using the collating sequence and can merge already sorted files and check if a file is sorted

sort can sort by numerical or alphabetical, applied to the entire input or by fields

```sh
# default alphabetical
sort <file>

#sort numerical
sort -n <file>

# eliminate duplicates with -u
sort -u <file>

# replace spaces with tabs and merge/sort the files
cat <file> | tr ' ' '\t' | sort - <file2>
```

uniq also eliminates duplicates

```sh
# remove duplicates of a particular field
uniq -f1 <file>

# count the number of duplicates
uniq -c <file>
```

## cut, paste and join

cut command extracts field from text, the default delimiter is a tab

```sh
# extract field 1
cut -f1 <file>

# change delimiter to : and select fields 1 and 7q
cut -d : -f 1,7 /etc/password
```

paste command pastes lines from two or more files side-by-side similar to pr -m

```sh
paste <file1> <file2>
```

join can join files based on a matching field

```sh
join -j 1 <file1> <file2>
```

## sed

stream editor is an extremely powerful tool.
Put simply sed loads lines from the input into the **pattern space** applies sed editing commands to the contents and sends to standard output.

Like other stream editors it can take a file as input or work as a filter.

```sh
# substitute first occurrence of a in each line
# s stands for sub, a is the matching item and A is the replacement
sed 's/a/A/' <file>

# to replace all occurrences of a in the file use g for global
sed 's/a/A/g' <file>

# the d is for delete, the preceding 2 indicates to delete the 2nd line only,  $ is for end of file
# a separator of ; for multiple commands
sed '2d;$s/a/A/g' <file>
```

In addition to operating on single lines sed can operate on ranges of lines.  

The beginning and end ranges are separated by a comma and can be specified by a number, regular expression or a $ for end of file.

You can group several commands between curly braces { } and use the -e option to add multiple commands to the script

```sh
# starting on line 2 until the $ end
sed -e '2,${' -e 's/a/A/g' -e '}' <file>
```

sed scripts can be stored in files

```sh
# store a space to tab conversion
echo -e "s/ /\t/g" > <sed-file>
sed -f <sed-file> <file>
```

sed using numbering lines

```sh
cat animals.txt
# example output
# animals:
#         aardvark
#         bat
#         cat
#         dog
#         emu
#         falcon

sed '=' animals.txt
# example output
# 1
# animals:
# 2
#         aardvark
# 3
#         bat
# 4
#         cat
# 5
#         dog
# 6
#         emu
# 7
#         falcon
```

add a second input to the **pattern space** using N and remove \n characters

```sh
sed '=' animals.txt | sed 'N;s/\n//'
# example output
# 1animals:
# 2       aardvark
# 3       bat
# 4       cat
# 5       dog
# 6       emu
# 7       falcon
```

edit the file in place

```sh
sed -i 's/\t/ /g' animals.txt
# example output
# $ cat animals.txt
# animals:
#  aardvark
#  bat
#  cat
#  dog
#  emu
#  falcon
```

## Pagers

Less has replaced more

```sh
# to be able to scroll up and down stdout
cat <file> | less
```
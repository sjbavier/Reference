# Working with grep

Common grep options 

```sh
grep -i # ignore case
grep -v # invert search
grep -c # count matches
grep -o # show only characters that match not full line
grep -r # recursive
grep -E # extended regex same as egrep
```

## Regex

```sh
# Achors
# ^   beginning
# $   end

# Matching characters
# .   any one character
# *   0 or more of the previous character

# Character sets
# [abc]  match characters a, b or c
# [0-9]  integers 0 - 9
# [a-z]  all characters a through z lowercase

# Character Classes
# [:graph:]    printable characters not including spaces
# [:print:]    printable characters including spaces
# [:punct:]    punctuation
# [:cntrl:]    non-printable control characters
# [:xdigit:]   hexadecimal characters

grep 'user[0-9]' <file>
# same as
grep 'user[[:digit:]]' <file>

# negating
grep 'user[![:digit:]]' <file>
```

## Extended Regex

```sh
# .   one character
# *   0 or more fo the previous character
# ?   0 or 1 of the previous character
# +   1 or more of the previous character
# {2}       two of the previous character
# {2,4}     two or four of the previous character
# (ab)      match a group of characters
# (ab){2}   two of the previous group
# (cat|dog) match cat or dog
```

## Grep uses [<https://unix.stackexchange.com/questions/17949/what-is-the-difference-between-grep-egrep-and-fgrep]>

grep -E and egrep are equivalent

```sh
# Interpret PATTERN as an ERE (Extended Regular Expression)
egrep
# and
grep -E
grep --extended-regexp
# are equal
```

grep -E switches grep into a special mode so that the expression is evaluated as an ERE (Extended Regular Expression) as opposed to its normal pattern matching.

```sh
# return lines that start with either "nofork" or "nogroup"
grep -E '^no(fork|group)' /etc/group
# same without -E flag note the escaped characters because of normal pattern matching
grep '^no\(fork\|group\)' /etc/group
```

grep -F and fgrep are equivalent

```sh
 # Interpret PATTERN as a list of fixed strings, separated by newlines, any of which is to be matched.

fgrep
# and
grep -F
grep --fixed-strings
# are equal
```

The -F switch switches grep into a different mode where it accepts a pattern to match, but then splits that pattern up into one search string per line and does an OR search on any of the strings without doing any special pattern matching.

```sh
# to search the group file with a plane text file list for any users listed in any group
grep -F -f user_list.txt /etc/group
```

Search all files recursively for specific text

```sh
grep -rnw '<path>' -e '<pattern>' # -r recursive, -n number, -w whole word
```

Find files containing give text

```sh
egrep -ir --include=*.{php,html,js} "(document.cookie|setcookie)" .
```

If you just want file names add the l (lowercase L) flag:

```sh
egrep -lir --include=*.{php,html,js} "(document.cookie|setcookie)" .
```

Grep showing lines before and after

```sh
# show 4 lines before and 4 lines after
cat <file> | grep -B 4 -A 4 <pattern>
```
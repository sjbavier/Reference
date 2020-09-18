# Working in Bash

- Grouping commands with {}

- Starting subshells with ()

- Use "" to prevent oddities

- Use [[]] for conditionals in modern bash

- In case statements ;; ;;& and ;& differences

- Using ; && and ||

## Some samples of common scripts

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

### Order of bootup **login** shell

Systemwide environment and shell variables
/etc/profile
/etc/profile.d/*.sh

User environment and shell variables
~/.bash_profile
~/.bashrc

Centos Only - systemwide aliases and shell functions
/etc/bashrc

Change shell to zsh

```sh
chsh -s $(which zsh)
```

View environment variables

```sh
printenv
```

Set an environment variable

```sh
export VARIABLE=VALUE
# remove the variable
export -n VARIABLE
```

Add a directory to PATH

```sh
# this is temporary unless added to .bashrc | .zshrc
export PATH="<directory-to-add>:$PATH"
```

Shell variables

```sh
# set a shell variable
VARIABLE=VALUE
# remove a shell variable
unset VARIABLE
```

## Conditionals

```sh
if CONDITION; then
   COMMANDS;
else
   OTHER-COMMANDS
fi

```

```sh
[ -a file ] #  file exists.
[ -d file ] #  file exists and is a directory[ -f file ] # file exists and is a regular file.
[ -u file ] # file exists and its SUID (set user ID) bit is set.
[ -g file ] # file exists and its SGID bit is set.
[ -k file ] # file exists and its sticky bit is set.
[ -r file ] # file exists and is readable.
[ -s file ] #  file exists and is not empty.
[ -w file ] # file exists and is writable.
[ -x file ] # is true if file exists and is executable.
[ string1 = string2 ] #  the strings are equal.
[ string1 != string2 ] # the strings are not equal.
[ int1 op int2 ] # where op is one of the following comparison operators:
-eq #  is true if int1 is equal to int2.
-ne #  true if int1 is not equal to int2.
-lt #  true if int1 is less than int2.
-le #  true if int1 is less than or equal to int2.
-gt #  true if int1 is greater than int2.
-ge #  true if int1 is greater than or equal to int2.
```

## For loops

```sh
for ITEM in SEQUENCE; do
   COMMANDS;
done
```

## While loops

```sh
while EVALUATION_CONDITIONAL; do
   COMMANDS;
done
```

## Directory Commands

```sh
mkdir <dirname>  # makes a new directory
cd               # changes to home
cd <dirname>     # changes directory
pwd              # tells you where you currently are
```
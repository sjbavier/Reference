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

**cat** is short for concatenate, used to display the contents of a file on stdout

```sh
cat <file>
# filter and redirect to another file
cat <file> | grep <pattern> > <file2>

# cat multiple files together such as file1 file2 etc. file*
cat <file>*
```

GNU text utilities come with **od** (octal dump)
Several options are available 
**-A** to control the radix of the file offets ( o, (octal, the default), d (decimal), x (hexadecimal), or n (no offsets displayed) )
 **-t** to control the form of the displayed contents


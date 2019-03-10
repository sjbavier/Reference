# Working with files

Display detailed information about a file

```sh
stat <file>
```

Matching a partial filename [matches file1, file2, ... file9 but not file10]

```sh
mv file? /some/other/directory
```

Matching a partial with wildcard * [all files that start with `file`]

```sh
cp file* /some/other/directory
```

Test if a file exists

```sh
test -f <file>
```

Compare two files

```sh
cmp -s <file1> <file2>
```

Unix file program, insider file information

```sh
file /sbin/int

    /sbin/init: symbolic link to /lib/systemd/systemd
```
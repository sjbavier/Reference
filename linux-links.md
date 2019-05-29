# Working with links

## Symbolic Links

To create a symbolic link from the file system object you want to link to the location you want the link to be placed

```sh
ln -s /nfs/home/ /home/username/Desktop
```

## Hard links

To create an exact duplicate of its target so that they will share a single inode ( metadata describing an object's attributes and location in the filesystem )

```sh
ln file1 file1-hard
```
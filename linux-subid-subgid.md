# subuid and subgid

/etc/subuid and /etc/subgid let you assign extra user ids and group ids.  After assigned they will no longer be available to other users or groups as their primary user or group ids, or for future assignment in /etc/subuid or /etc/subgid.

The user "owns" the assigned **ids** and can change ownership of the files and processes running under these ids.

in /etc/subuid and /etc/subgid you can assign blocks of ids to users.

```conf
# /etc/subid
<user>:100000:65536
# format
<user>:<start-block><number-count>
```

Normally Linux systems use ids between 0 and 65536 but the allowed **UID** and **GID** space is much greater. 

This is particularly userful in containers for isolation as a way to shift the range of UIDs and GIDs in the container so they are not shared with the UIDs and GIDs of the host system.  If the user were to escape the container and has root access their UID would be 100000 and not 0 and would be denied access by default.



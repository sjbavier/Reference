# Working with tmux

Listing sessions

```sh
tmux list-sessions
```

Start a new session with name

```sh
tmux new-session -s <session-name>
```

Attach session

```sh
tmux a -t <session-name>
```

## Within tmux session

Detach current session

```sh
tmux detach
```

Split pane vertically [ctrl + b %]

Split pane  horizontally [ctrl + b "]

Resizing pane [ctrl + b :resize-pane (U, D, L, R) #]

Scrolling [ ctrl + b + [ ]
   exit scrolling [ ctrl + c ]

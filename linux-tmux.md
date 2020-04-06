# Working with tmux

Listing sessions

```sh
tmux list-sessions
tmux ls
```

Start a new session with name

```sh
tmux new-session -s <session-name>
tmux new -s <session-name>
```

Attach session

```sh
tmux a -t <session-name>
tmux at -t <session-name>
tmux attach -t <session-name>
tmux attach-session -t <session-name>
```

Kill session

```sh
tmux kill-session -t <session-name>
tmux kill-ses -t <session-name>
# kill all sessions but the current
tmux kill-session -a
# kill all sessions but named session
tmux kill-session -a -t <session-name>
```

## Within tmux session

Detach current session

```sh
tmux detach
# or ctrl+b d
```

Split pane vertically 
[ctrl + b %]

Split pane  horizontally 
[ctrl + b "]

Resizing pane 
[ctrl + b :resize-pane (U, D, L, R) #]

Scrolling 
[ ctrl + b + [ ]
exit scrolling 
[ q, ctrl + c ]

Rename session
[ctrl + b $]

Toggle pane zoom
[ctrl + b z]
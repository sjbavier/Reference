# Working with Git

Initialize git within current directory

```sh
git init
```

## Configuring git

## Working with branches

Delete a branch

```sh
git branch -D <branch>
```

View branches

```sh
git branch
```

Make a branch

```sh
git checkout -b <branch>
```

Switch to a branch

```sh
git checkout <branch>
```

Discard all local changes to all files permanently 

```sh
git reset --hard
```

## Rebase master branch

To stash current changes and rebase master

```sh
# stash the current front-end branch
git stash

# checkout master
git checkout master

# perform git pull to update master
git pull

# switch back to <branch>
git checkout <branch>

# rebase front-end with newest master branch
git rebase master

# force push stash
git push -f

# array pop last stash entry?
git stash pop
```

Reset the local branch to the remove

```sh
# fetch remote origin
git fetch origin

# hard reset local to remote origin
# set the current branch head (HEAD) to <commit>, optionally modifying index and working tree to match. The <commit> defaults to HEAD in all forms.
git reset --hard <commit>

# example
git reset --hard origin/master
```

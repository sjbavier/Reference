# Working with Git

## Semantic Versioning

Format MAJOR.MINOR.PATCH (eg. 1.0.6)

- MAJOR version when you make incompatible API changes,
- MINOR version when you add functionality in a backwardcompatible manner, and
- PATCH version when you make backward-compatible bug fixes.

## Configuring git

Configure username and email globally

```sh
git config --global user.name "<username>"
git config --global user.email "<email>"
```

Initialize git within current directory

```sh
git init
```

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

Abort a merge

```sh
git merge --abort
```

## Add existing local project to remote repository

```sh
# set the new remote
git remote add origin <remote-repo-url>
# verify the remote repository
git remote -v
# push the changes to remote
git push origin master
```

## Add a git version tag

```sh
git tag -a "v0.0.1" first release of foo
git push --follow-tags
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

## Discarding local changes

Stash the changes

```sh
# --include-untracked optional
git stash save --keep-index --include-untracked
```

Drop the stash

```sh
git stash drop
```


## Gitignore [.gitgnore]

To remove files after they have been added, try clearing the cache. 

```sh
git rm --cached -r . 
git add .
git status
```

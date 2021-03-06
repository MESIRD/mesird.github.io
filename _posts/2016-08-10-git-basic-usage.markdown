---
layout: post
title:  "Git basic usage"
date:   2016-08-10 19:12:20
categories: Git
tags: Git
---

## basic
**git status**
*show status of current branch*

* `git status -s` shows the short message of current branch

**git add**
*make unstaged file staged (append filename)*

* `git add --all` make all files

**git diff**
*show what you've changed but not yet staged (append filename)*

* `git diff --staged` & `git diff --cached` show the difference between staged and last committed files

**git commit**
*commit staged files*

* `git commit -m "bug fixed"` commit staged files using single line command
* `git commit -a -m "but fixed"` commit unstaged but tracked file directly

**git rm**
*remove and stage this removal*

* `git rm -f` force remove file that has been added to index
* `git rm -cached` remove file from tracking but still on disk
* `git rm log/\*.log` remove all .log file in log directory

**git mv**
*move or rename a file*

**git log**
*viewing commit history*

* `git log -p` show the difference introduced in each commit
* `git log -p -2` limit difference to 2 entries
* `git log --stat` show logs with modified files and total modified file count of each commit
* `git log --shortstat` show logs with total modified file count of each commit
* `git log --name-only` show logs only with modified file names
* `git log --name-status` show logs with modified file names and file status
* `git log --abbrev-commit` show logs with few characters of SHA-1 checksum
* `git log --relative-date` show logs with date in relative format("18 minutes ago")
* `git log --pretty=oneline` show logs in one line format
* `git log --pretty=format:"%h - %an, %ar : %s"` show logs in custom format
* `git log --oneline --decorate` show logs with where the branch pointers are pointing

| Option | Description of Output |
| --- | --- |
| %H | Commit hash |
| %h | Abbreviated commit hash |
| %T | Tree hash |
| %t | Abbreviated tree hash |
| %P | Parent hashes |
| %p | Abbreviated parent hashes |
| %an | Author name |
| %ae | Author email |
| %ad | Author date (format respects the —date=option) |
| %ar | Author date, relative |
| %cn | Committer name |
| %ce | Committer email |
| %cd | Committer date |
| %cr | Committer date, relative |
| %s | Subject |

> `author` is the person who modifies the file, `committer` is who make the commit

* `git log --pretty=oneline --graph` show log with ascii graph
* `git log --since "2 years 1 day 3 minutes ago"` & `git log --after "2016/7/21"` show logs since the specified date
* `git log --until "1 day ago"` & `git log --before "2016/7/20"` show logs until the specified date
* `git log --author mesird` show logs that filtered by author name
* `git log --committer mesird` show logs that filtered by committer name
* `git log --grep bugfix` show logs filtered by commit message
* `git log -S getEnterpriseIPADownloadUrl` show logs filtered by modified code

## config
**git config --global user.username**
*show or modify git global username*

**git config --global user.email**
*show or modify git global email*

**git config --global core.editor**
*change git editor (vim or emacs)*

**git config --global alias.co checkout**
*using `co` to replace `checkout`, e.g. `git co`*

## branching
**git branch**
*show local branch list*

* `git branch -v` show local branch list with last commit
* `git branch -vv` show local branch list with tracked upstream branch and last commit
* `git branch [branch-name]` create a new local branch
* `git branch -d [branch-name]` delete a branch
* `git branch -D [branch-name]` force delete a branch
* `git branch --merged` show local branch list that has been merged into current branch
* `git branch --no-merged` show local branch list that hasn't been merged into current branch yet


**git checkout [branch-name]**
*switch to the particular branch, this command will move HEAD pointer to the current branch*

* `git checkout -b [branch-name]` create and switch to the particular branch
* `git checkout -b [branch-name] [remote-branch-name]` create a new branch copied from a remote branch and switch to the new branch
* `git checkout --track [remote-branch-name]` make track relationship between current branch and the particular remote branch

**git merge [branch-name]**
*merge the particular branch to current branch*

**git mergetool**
*open a visual conflict resolving tool*

* `git mergetool -tool=[toolname]` configure a merge tool

**git ls-remote [remote-name]**
*show full list of remote references*








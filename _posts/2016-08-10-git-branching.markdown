---
layout: post
title:  "Git Branching"
date:   2016-08-10 19:12:20
categories: Git
tags: Git
---

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








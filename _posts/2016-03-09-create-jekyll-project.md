---
layout: post
title:  "Create jekyll project on mac"
date:   2016-03-09 17:59:20 +0800
author: "mesird"
---

[Jekyll Quick Start](https://jekyllrb.com/docs/quickstart)

## first step
download jekyll on your mac using following command  
```
gem install jekyll
```

## second step
create jekyll in an existing folder with some files (like a git repo)  
```
jekyll new . --force
```

**or*

create jekyll in a new folder  
```
jekyll new [folder name]
```

there're several folders and files that would be created after jekyll set up, project would be like this(*README.md is a file created by github*):  
![project](/images/project_list.png)

**_config.yml**  
you can config your project with some global variables in `_config.yml`, like website title, description etc.

**_includes**  
this is an folder contains web components like header or footer.

**_layouts**  
this folder has some basic layout for Home, Post or other pages, you can custom your own layout in this folder.

**_posts**  
Your posts would be stored in this folder.

**_sass**  
I don't know what does this folder work currently...

**about.md**  
This is your about page, which might using certain layout.

**css**  
Your style files(css) would be stored in this folder.

**feed.xml**  
I don't know at present.

**images**  
this folder is created by myself, you can name it some other ways like `resources` or `assets`.

**index.html**  
This is your Home page.

finally the page sample with default style would be like this.  
![sample_page](/images/sample_page.png)

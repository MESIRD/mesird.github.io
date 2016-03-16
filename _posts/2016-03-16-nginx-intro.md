---
layout: post
title:  "nginx intro"
date:   2016-03-16 09:46:20 +0800
author: "mesird"
---
**Start**  
`./nginx`

**Stop**  
`./nginx -s stop`

**Reload**  
`./nginx -s reload`

**Validate nginx.conf file**  
`./nginx -t`

**location**  
`=` 表示精确匹配,这个优先级也是最高的  
`^~` 表示 uri 以某个常规字符串开头,理解为匹配 url 路径即可。nginx 不对 url 做编码,因此请求为 /static/20%/aa,可以被规则^~ /static/ /aa 匹配到(注意是空格)  
`~` 表示区分大小写的正则匹配  
`~*` 表示不区分大小写的正则匹配(和上面的唯一区别就是大小写)  
`!~`和`!~*` 分别为区分大小写不匹配及不区分大小写不匹配的正则  
`/` 通用匹配,任何请求都会匹配到,默认匹配


**Root** `path/uri`  
Syntax: `root path`  
default : `root html`  
```
location ^~ /admin/ {
    root /local/;
    autoindex on;
    ...
}
```  
如果URI为 `/admin/invest/queryList.json`，服务器会返回`/local/admin/invest/queryList.json` 

**Alias** `path-location/uri`  
Syntax: `alias path`  
```
location ^~ /admin/ {
    limit_conn limit 4;
    limit_rate 200k;
    internal;
    alias /web/;
}
```   
如果URI为 `/admin/invest/queryList.json`，服务器会返回`/web/invest/queryList.json`
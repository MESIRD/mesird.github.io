#!/usr/bin/python
# -*- coding: UTF-8 -*-

import urllib
import urllib2
import json

get_url = "http://192.168.0.1/userRpm/AssignedIpAddrListRpm.htm"
headers = {
    "Host": "192.168.0.1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Referer": "http://192.168.0.1/userRpm/MenuRpm.htm",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4",
    "Cookie": "Authorization=Basic%20YWRtaW46NTEwNTEwNTEw; ChgPwdSubTag="
}
req1 = urllib2.Request(url=get_url, headers=headers)
res_data1 = urllib2.urlopen(req1)
html1 = res_data1.read()
# html = unicode(html, "gb2312").encode("utf8")
personIsAtHome = []
personIsntAtHome = []
info = ""
if html1.find("Mesirds-iPhone7") > 0:
    personIsAtHome.append("杰宝")
else:
    personIsntAtHome.append("杰宝")
if html1.find("liunan") > 0:
    personIsAtHome.append("楠狗")
else:
    personIsntAtHome.append("楠狗")
if html1.find("sunxuesdeiPhone") > 0:
    personIsAtHome.append("孙神")
else:
    personIsntAtHome.append("孙神")
if html1.find("wangrubing") > 0:
    personIsAtHome.append("小冰冰")
else:
    personIsntAtHome.append("小冰冰")
if html1.find("iPhone-3") > 0:
    personIsAtHome.append("小妹妹")
else:
    personIsntAtHome.append("小妹妹")
if len(personIsAtHome) > 0:
    separator = "，"
    atHomeInfo = separator.join(personIsAtHome)
    atHomeInfo += "都已经到家了\n"
    info += atHomeInfo

if len(personIsntAtHome) > 0:
    separator = "，"
    isntAtHomeInfo = separator.join(personIsntAtHome)
    isntAtHomeInfo += "还没回来呢"
    info += isntAtHomeInfo

post_url = "https://oapi.dingtalk.com/robot/send?access_token=067220ac1db35328a475ececb6ab6d30f8a6a2761e600162e820c8c22c3ff536"
post_headers = {
    "Host": "oapi.dingtalk.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "Content-Type": "application/json",
}
post_data = {
    "msgtype": "text",
    "text": {
        "content": info
    }
}
json_data = json.dumps(post_data)
# post_data_url_encoded = urllib.urlencode(post_data)
req2 = urllib2.Request(url=post_url, data=json_data, headers=post_headers)
res_data2 = urllib2.urlopen(req2)
res2 = res_data2.read()
print res2
---
layout: post
title:  "JSPatch simple usage"
date:   2016-07-11 16:07:10 +0800
author: "mesird"
---

## introduction
**official introduction**   [Github/JSPatch](https://github.com/bang590/JSPatch)
> JSPatch bridges Objective-C and JavaScript using the Objective-C runtime. You can call any Objective-C class and method in JavaScript by just including a small engine. That makes the APP obtaining the power of script language: add modules or replacing Objective-C code to fix bugs dynamically.

## import
**cocoapods**
*you can add `pod 'JSPatch', '~> 1.0'` in your Podfile, run `pod install`
**framework**
*download JSPatch SDK from [JSPatch platform](http://www.jspatch.com/Index/sdk), then add this framework into your project*
**files**
*download JSPatch project on [Github/JSPatch](https://github.com/bang590/JSPatch), then copy `JSPatch.js`, `JPEngine.h`, `JPEngine.m` three files to your project*

## before starting
JSPatch needs `libz.dylib` and `JavaScriptCore.framework`, thus import the two framework.
## start
**local**
* add a javascript file to your project
* add your own JSPatch code in js file
* add following code at the most beginning position your application initialize, basically we add at the beginning of `application:didFinishLaunchingWithOptions:`.

```
[JPEngine startEngine];
NSString *scriptPath = [[[NSBundle mainBundle] bundlePath] stringByAppendingPathComponent:@"main.js"];
[JPEngine evaluateScriptWithPath:scriptPath];
```

**JSPatch platform**
* add following code at the beginning of the method `application:didFinishLaunchingWithOptions:`

```
[JSPatch startWithAppKey:appKey];   // appKey is offer on JSPatch platform
[JSPatch sync];
```
## syntax
**[official document - basic usage](https://github.com/bang590/JSPatch/wiki/JSPatch-基础用法)**
**require**

before using every OC-defined object, you need to use `require` syntax to get the privilege of use, like this 

```
require('UIColor')
UIColor.whiteColor()
```

you can also require multi-class together

```
require('UIColor,UIFont,UILabel')
UIColor.whiteColor()
UIFont.systemFontSize()
UILabel.alloc().init()
```

also using require directly

```
require('UIColor').whiteColor()
```

**defineClass**

whenever you want to replace a method in a class, you need to use `defineClass` to get the privilege of this class, the parameters are explained below

```
defineClass('ClassName', [newParameter1, newParameter2], {instance methods}, {class methods})
```

a simple demo here

```
defineClass('MHCB2BHomeViewController', [blankView], {
    viewDidLoad : function() {
        self.super().viewDidLoad()
        // any additional operation
        self.setBlankView(require('MHCB2BGeneralBlankView').alloc().init());
        self.blankView().setHidden(YES);
    },
    viewDidAppear : function() {
        self.ORIGviewDidAppear()
        // any additional operation
    }
})
```

**method**

* method should be invoked using a couple of brackets after, get/set properties should using their getter/setter

```
var label = UILabel.alloc().init()
label.setText('This is title')
label.text()
```

* method with parameters

```
var indexPath = require('NSIndexPath').indexPathForRow_inSection(0,1)
```

* invoke original method in OC, add `ORIG-` prefix

```
viewDidLoad : function() {
    self.ORIGviewDidLoad()
    // some additional operation
}
```

**special types (struct)**

```
// create struct
var frame = {x:20, y:20, width:100, height:100}
var point = {x:20, y:20}
var size  = {width:100, height:100}
var range = {location:0, length:1}

// get variable
var x = self.view().frame().x
var width = self.view().frame().width
```

**selector**

```
...
if (self.delegate()) {
    self.delegate().performSelector("listView_didSelectItem", self, item);
}
...
```

**block**

* block with no parameter

```
var slf = self
var blk = block(function() {
    slf.queryBrands()
})
```

* block with parameters

```
require('NSError, MHCB2BProgressHUD, NSDictionary')
var slf = self
var blk = block("BOOL, NSDictionary*, NSError*", function(succeed, result, error) {
    if (succeed) {
        // some code here
    } else {
        MHCB2BProgressHUD.showErrorWithText(error.localizedDescription())
    }
})
```

**GCD**

```
dispatch_after(1.0, function() {
    // some operation
})

dispatch_async_main(function() {
    // some operation
})

dispatch_sync_main(function() {
    // some operation
})

dispatch_async_global_queue(function() {
    // some operation
})
```

**debug**

* printing log message in console

```
console.log('some text')    // print a string
console.log(object)         // print an object
```

* setting breakpoint in js file, following the [tutorial](https://github.com/bang590/JSPatch/wiki/JS-断点调试)

## principle
**[official document - implementation principle](https://github.com/bang590/JSPatch/wiki/JSPatch-实现原理详解)**


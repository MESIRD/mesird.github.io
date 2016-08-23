---
layout: post
title:  "iOS debugging techs"
date:   2016-08-23 13:43:20
categories: iOS
tags: iOS
---

> Everyone knows that debugging is twice as hard as writing a program in the first place. So if you're as clever as you can be when you write it, how will you ever debug it?           
> --- Brian Kernighan

在一个项目推进的过程中，不论是在开发中或是提测后，程序总是会出现一些非我们所期待的结果，更严重者崩溃，因此我们需要去逐行排查问题代码的根源，此时我们需要用到自身的调试能力。    
往往一个开发人员排查错误代码的能力能体现出其编程水平的高低。    
首先我以个人认知将iOS开发的调试分为以下几类：

* 代码调试
* UI调试
* 性能调优
* JSPatch调试

## 代码调试

> 代码调试被视作开发人员必备技能，但是大多数人掌握的也只是简单查看变量的值，因此掌握更全面的代码调试技巧会对你在今后的开发过程中有更大的帮助。

### 断点调试(Breakpoint)

**当程序执行到断点处，你有4种操作可以继续调试**    

1. 继续执行(continue program execution)    
    *该操作将继续执行程序，一直到下次碰到断点后再停止。*    
2. 单步调试(step over)    
    *该操作将程序当前的位置向下执行一行。*    
3. 进入方法体(step in)    
    *若当前程序位置所在行有可以进入的方法体，该操作将进入该方法体。*    
4. 走出方法体(step out)    
    *若当前程序位置所在行在某个方法内，该操作将直接跳出该方法。*    

#### 局部断点(Local)

*在需要单步调试的地方设置局部断点，当程序执行到相关代码时会定位到对应的代码行*

**添加断点**

1. 点击代码编辑器的左侧行数，添加断点
    ![](/images/ios-debugging-techs/add_line_breakpoint.jpg)
2. 将光标移动至需要添加断点的行，按下快捷键`command` + `\`

**查看断点**

* 展开XCode的导航器(Navigator)，点击Breakpoint Navigator选项查看所有断点
    ![](/images/ios-debugging-techs/show_breakpoint_navigator.jpg)

**设置断点是否有效**

* 点击断点图标即可设置是否有效
    ![](/images/ios-debugging-techs/enable_breakpoint.jpg)

#### 全局断点(Global)

*全局断点指在整个应用运行期间，一旦满足某个条件，程序即定位到触发该条件的代码行*

![](/images/ios-debugging-techs/global_breakpoint.jpg)

**崩溃断点(Exception)**

* 在Breakpoint Navigator底部点击`+`按钮，选择`Add Exception Breakpoint...`    
* 应用崩溃时，程序定位到最后导致崩溃的代码行
    
**符号断点(Symbolic)**

* 在Breakpoint Navigator底部点击`+`按钮，选择`Add Symbolic Breakpoint...`
* 当执行到带有该符号的代码时，进入调试环境

#### 条件断点(Conditional)

*通过局部添加断点，可以给断点设置过滤条件，满足条件时程序才会进入断点调试模式*

**添加过滤条件(condition)**

* 右键断点图标，选择`Edit Breakpoint...`
* 在condition输入框中添加判断条件，当条件返回`YES`时，进入调试状态

**设置忽略次数(ignore)**

* 在Ignore输入框中输入你需要忽略的次数，只有能够触发断点的情况才算是可以被忽略，也就是说忽略满足条件的次数

**设置断点行为(action)**

断点包括以下几种行为

* AppleScript    
    嵌入AppleScript代码并执行
* Capture GPU Frame
    捕获当前GPU绘制的帧
* Debugger Command    
    执行LLDB命令，如 `po size`，`bt`，`expression i = 93`
* Log Message    
    打印信息到控制台，`%B` 打印断点名称，`%H` 打印断点调用次数，在`@@`之间输入表达式
* Shell Command
* Sound    
    在断点捕捉到时，播放一个音效

![](/images/ios-debugging-techs/breakpoint_action_1.jpg)

**用途**

我们经常会为代码中有太多的NSLog而烦恼，在需要时去写一个，不需要时去删除亦或是注释掉，不仅仅让代码看上去凌乱不堪而且添加了管理成本。现在，我们可以使用断点来提供打印功能。

在需要做输出的地方添加断点，并选择Action为`Log Message`，然后将你需要输出的内容添加到输入框中，并选中`Automatically continue after evaluating actions`（选中此项表示程序走到该断点处不会进入调试模式，而是处理完action后继续程序执行）。

在程序正在运行中，若想查看代码执行到某个地方的变量值时，通过这种方法就可以不需要重新编译一遍项目，只需要添加一个断点即可。

当不需要输出时，只需要将该断点设置为无效即可。    
![](/images/ios-debugging-techs/breakpoint_action_2.jpg)

### LLDB

// FIXME

**调试命令**

* `n/next`      step over, F6
* `s/step`      step in, fn + F7
* `finish`      step out, fn + F8
* `c/continue`  goto next breakpoint, `^` + `⌘` + `Y`
* `expr/expression` evaluate a C/Objective-C/C++ expression(动态执行表达式)    
    * `expr [self.view setBackgroundColor:[UIColor redColor]]`
* `p/print`     print as a C/C++ basic variable
* `po/expr -O`  print as an Objective-C object
* `call`        call a method
    * `call [self.view setBackgroundColor:[UIColor redColor]]`
* `bt`          print backtrace(打印堆栈回溯)
* `image`       find code line that corresponding to specified stack(寻找栈所对应的代码行)
    * `image lookup --address 0x000000010c95093b`
* `x/mem read`  read from the memory of the process being debugged(dump 指定地址的内存)
* `mem write`   write to the memory of the process being debugged(改写指定地址的内存)

**小技巧**

有的时候在`po`(print object)一个对象的时候，控制台会报错提示无法打印，这个时候你只要将输出对象进行强制转换即可

如`po (CGRect)self.view.frame`

## UI调试(User Interface)

很多情况下，sb(storyboard)、xib或是代码写好的UI控件，但在项目跑起来后却找不到或是位置、大小、颜色、约束等属性不正确，这时候一般会去再次查看sb、xib及代码的正确性，大多数情况下在认真的检查后都能找到问题所在。然而还有小部分情况下，依然很难找到问题所在，如：一个控件不显示，但是代码里面没有找到设置hidden的地方，但其实是由于层级关系被上层view所遮挡；设置好一个图片控件，添加的单击手势，可是怎么点击图片都不触发回调方法，其实是没有设置imageView的userInteractiveEnable属性为YES，等等。所以在这种对UI调整精度要求较高的情况下，我们可以采用多种UI调试的方法达到我们所想要的结果。

UI调试工具种类繁多，在此我介绍两款我使用过并极力推荐的UI调试应用：

### Reveal

> Reveal brings powerful runtime view debugging to iOS developers. With advanced visualizations, comprehensive inspectors and the ability to modify applications on the fly, you’ll be debugging view layout and rendering problems in seconds.

> Reveal给iOS开发者带来了强大的运行时视图调试功能。它拥有先进的可视化、全方面的检查器以及实时修改应用程序的能力，可以让你在分分钟内调试各种视图布局以及渲染问题。

**项目环境配置**

1. 添加Reveal.framework: 启动Reveal --> Help --> Show Reveal Library in Finder,拖动添加Reveal.framework到工程中（Copy item if needed）
2. 添加其他Library: `CFNetwork.framework`, `QuartzCore.framework`, `CoreGraphics.framework`
3. 设置Target: TARGETS --> Settings --> Other Linker Flags -->添加命令 `-ObjC -lz -framework Reveal`
4. 若真机调试，保证与Mac在同一WiFi环境下

若以上步骤操作完依然不生效，参考[官方文档 - 集成Reveal：静态连接](http://support.revealapp.com/kb/getting-started/reveal-2)

**查看界面层级**

![](/images/ios-debugging-techs/reveal.jpg)

左侧导航器中，展示了所有界面中存在的View，中间主窗口为3D效果的界面展示，可以通过拖拽、缩放、平移进行交互，右侧为选中控件的属性展示。接下来我将详细介绍一下关于Reveal的使用方法。

<img src="/images/ios-debugging-techs/reveal_left.jpg" width=60% />

当你成功运行一个App后，若Reveal没有自动载入，你可以点击红色方框对应按钮，选择你当前正在运行的项目，Reveal就会将该App对应的视图层级加载到主界面中。下方以包含关系列出了所有视图，双击某个视图将其单独显示在主视图中，点击红色方框左侧的左箭头返回上一级视图，点击红色箭头所指按钮可以查看约束信息。

<img src="/images/ios-debugging-techs/reveal_main.jpg" width=60% />

在主界面中，你可以看到当前App运行的界面层级，顶部按钮从左到右依次是 线框、原视图、线框+原视图、缩放比例、正视图及3D视图。在主界面中，左右拖拽可以在不同角度查看，点击某个视图，会将该视图属性展示在右侧的属性检查器中。

![](/images/ios-debugging-techs/reveal_right_1.jpg)
![](/images/ios-debugging-techs/reveal_right_2.jpg)
![](/images/ios-debugging-techs/reveal_right_3.jpg)
![](/images/ios-debugging-techs/reveal_right_4.jpg)
![](/images/ios-debugging-techs/reveal_right_5.jpg)

属性检查器的能力非常强大，几乎可以修改所有关于视图相关的内容。以下是每个检查器所能查看及修改的内容：

* 应用检查器 (Application Inspector) - *包含应用层面相关的属性，以及设备信息*
    * 图标Badge数字 (Icon Badge Number)
    * 状态栏 (Status Bar)
    * 设备信息 (Device)
* 标识符检查器 (Identifier Inspector) - *所选控件对应的类、内存信息等*
* 属性检查器 (Attributed Inspector) - *根据不同的控件，对应的属性也不相同，如UILabel会有Text, Color, Font, Alignment等属性*
* 布局检查器 (Layout Inspector) - *视图大小、位置、约束信息*
* 图层检查器 (Layer Inspector) - *选择的视图对应的CALayer属性*

更多的使用技巧在实际应用中会慢慢掌握，也可以访问 [Reveal Knowledge Base](http://support.revealapp.com/kb) 查询更多资料

### Xcode - Debug View Hierarchy

在Xcode 6中，苹果引入了强大的视图调试工具。在调试状态下，点击 Debug --> View Debugging --> Capture View Hierarchy 

![](/images/ios-debugging-techs/xcode_ui_menu.png)

或是直接点击调试工具栏的视图调试按钮进入视图调试。

![](/images/ios-debugging-techs/xcode_ui_tool.jpg)

启动后，如Reveal相同，可以查看App当前视图层级的3D展示

![](/images/ios-debugging-techs/xcode_main.jpg)

左侧依然是视图层级列表，默认包含了约束信息（若默认不是展示视图列表，需要选择`View UI Hierarchy`）

![](/images/ios-debugging-techs/xcode_left.jpg)

选择一个控件后，对象检查器(Object Inspector)与尺寸检查器(Size Inspector)中展示了相关信息，但仅仅只能查看不支持修改。

![](/images/ios-debugging-techs/xcode_right_1.jpg)
![](/images/ios-debugging-techs/xcode_right_2.jpg)

**两者对比：**

1. Xcode调试UI时，无法在真机或模拟器上进行交互，相较而言Reveal则并不影响真机或模拟器上App的运行与用户操作，若需要再次获取视图层级时，只需要在Reveal中刷新即可，这点来说Xcode略显不足。
2. Reveal在调试UI过程中，可以在属性检查器中查看并修改控件的相关属性，并且即时生效（不得不说这点非常强大），而Xcode在调试时并不能在属性检查器中修改属性，但是可以通过LLDB命令去修改（在之前已有介绍），不过不能即时生效，而是在结束界面调试后才能生效



## 性能调优()

// FIXME







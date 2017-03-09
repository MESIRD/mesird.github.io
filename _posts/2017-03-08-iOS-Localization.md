---
layout: post
title:  "iOS Localization"
date:   2017-03-08 21:12:20
categories: iOS
tags: iOS
---

## Introduction

Recently, most apps on App Store is 

## Make you app localizable!

**Step 1 : Create a `strings` file**

Right click a group (Supporting Files is recommended) and select `New File...`, Find `Strings File` in the `iOS -> Resource` category. Remember to name it `Localizable.strings` which is the default name for the localizable file.

![pi](/images/ios-localization/create-strings-file.png)

**Step 2 : Make it localizable**

Click `Localize...` button on the right side of screen, this action is to make `.strings` file localizable, thus you can add languages to it.

![pi](/images/ios-localization/localize.png)

**Step 3 : Add languages you need to it**

Select your project file (in my project it's MSDLocalizationDemo), then select project item which is the same name as your project file. Click `+` in `Locaizations` block, and select language you want. 

![pi](/images/ios-localization/add-languages.png)

Then select `Localizable.strings` file to finish adding.

![pi](/images/ios-localization/select-file-to-localize.png)

**Step 4 : Add your localized text**

![pi](/images/ios-localization/file-directory.png)

```objc
// in 'Localizable.string - English' file
"HomeLabelText" = "This is home screen";

// in 'Localizable.string - Chinese(Simplified)' file
"HomeLabelText" = "这是首页";

// in 'ViewController'
_label.text = NSLocalizedString(@"HomeLabelText", nil);
```

### Debug your localizable strings

There are some options you can select in current scheme before running the project, we can see them in `Edit Scheme...` -> `Options`.

#### Show non-localized strings

Turn on `Show non-localized strings` option, you will get all strings that are not localized in your `Localizable.strings` file in console like this:

```
2017-03-09 13:24:56.262468 MSDLocalizationDemo[14029:952398] [strings] ERROR: LabelText1 not found in table Localizable of bundle CFBundle 0x7fe0e4600930 </Users/mesird/Library/Developer/CoreSimulator/Devices/68C6EB61-BC3D-4173-8997-6562D124C250/data/Containers/Bundle/Application/1B262849-AB7C-43F2-A7E4-F70E525A07CA/MSDLocalizationDemo.app> (executable, loaded)
```

`LabelText1` is not defined in my Localizable file, so it would be print out.

#### Change application language

Select the language you expect listed in the options, app will display text in this language after next launch.

## Localization in cocoapods




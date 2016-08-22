---
layout: post
title:  "Effective Objective-C 2.0"
date:   2016-06-07 10:45:10
categories: Objective-C
tags: Objective-C
---

1. Familiarize yourself with Objective-C’s Roots

    * method calling is based on messaging
    * Objective-C object is stored on Heap whereas struct object as basic type data is stored on Stack

2. Minimize Importing Headers in Headers

    * using `@class` rather than `#import`
    * moving protocol-conformance declaration to class-continuation category is better
    * importing header files in implementation as possible as your can

3. Prefer Literal Syntax over the Equivalent Methods

    * define Objective-C objects with Literal Syntax like    
    
    ```
    NSNumber *maxCount = @3;  
    NSString *userName = @“Nick”;  
    NSArray *animals = @[@“fox”, @“chicken”, @“cat”];  
    NSString *fox = animals[0];  
    NSDictionary *personInfo = @{@“firstName”:@“Nick”, @“lastName”:@“Ben”, @“age”, @18};
    ```
    
4. Prefer Typed Constants to Preprocessor #define

    * using constant rather than preprocessor
    
    ```
    #define DURATION = 0.5; [this is worse]
    static const NSTimeInterval kTimeDuration = 0.5f; [this is better]
    extern static variable
    extern NSString *const kOptionUserInfoTarget; [in header file]
    NSString *const KOptionUserInfoTarget = @“OptionUserInfoTarget”; [in implementation file]
    ```

5. Use Enumerations for States, Options, and Status Codes

    * enumeration definition
    
    ```
    typedef NS_ENUM(NSInteger, MSHUDType) {
        MSHUDTypeGeneral	= 0,
        MSHUDTypeText 	= 1,
        MSHUDTypeCompletion = 2,
        MSHUDTypeError 	= 3
    }
    ```
    
    * option definition

    ```
    typedef NS_OPTIONS(NSInteger, MSAlertComponent) {
        MSAlertComponentTitle = 1 << 0,
        MSAlertComponentContent = 1 << 1,
        MSAlertComponentButton = 1 << 2
    }
    ```

6. Understand Properties

    * attributes
        * readwrite : both a getter and a setter are available
        * readonly  : only a getter is available
        * assign    : simple assign operation used for scalar types (CGFloat, NSInteger)
           
        ```
        newValue = oldValue;
        ```
           
        * strong    : the property defines an owning relationship
           
        ```
        newValue = oldValue;
        [newValue retain];
        [oldValue release];
        ```
           
        * weak      : the property defines a nonowning relationship (just like what assign does), value is nilled out when object is destroyed
      
        ```
        newValue = oldValue;
        ```
      
        * unsafe_unretained : the property defines a nonowning relationship, value is not nilled out when target is destroyed
   
        ```
        newValue = oldValue;
        ```
      
        * copy      : the property defines an owning relationship, it is a copy of the target (different memory address)
           
        ```
        newValue = [oldValue copy];
        ```
    
7. Access Instance Variables Primarily Directly When Accessing

    * Them Internally
        * direct access on properties
            * undoubtedly faster
            * will not cause property attribute like copy action (copy
              action will be translated as following codes)
            
            ```
            newValue = oldValue;
            [newValue retain];
            [[oldValue release];
            ```
    
            * key-value observing(KVO) will not be fired (whether it is
       correct or not depending on what you want)
            * easy to debug 

8. Understand Object Equality

    * Equality
        * ‘ == ‘  : whether the two objects own the same address
        * isEqual : whether the two objects have the same hash
        * isEqualToString : whether the two strings have same content
    * NSSet
    
    ```
    aSet = {((1,2), (1,2))}
    bSet = [aSet copy]; // bSet is {((1,2))}
    ```
       
9. Use the Class Cluster Pattern to Hide Implementation Detail
10. Use Associated Objects to Attach Custom Data to Existing Classes
11. Understand the Role of objc_msgSend
12. Understand Message Forwarding



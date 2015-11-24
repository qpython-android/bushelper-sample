[TOC]

# 公交路线查询移动应用系统- QPython WebApp版本

搜索关键字：
-----

- QPython
- WebApp
- html5
- Web前端框架



概述
-----
在移动互联网应用开发的大潮中，有那么一种技术一直都在以主角的身份不断吸引诸多开发者的关注，它就是WebApp技术，和原生开发相比，WebApp能够快速兼容Web开发模式，快速上手，部署更新简单的优势得到了非常多的开发者的青睐。

QPython的WebApp方案就是众多WebApp方案中的极为优秀的一种，QPython 的 WEB APP 方案有以下优势：

- 强大的本地逻辑处理解析器：Python 脚本解析器
QPython 有一个强大的本地逻辑处理解析器，能在你的手机端进行进（线）程运算、图形处理及渲染、进行多种协议的网络通讯等工作，这样不需要提交给云端就能充分地利用了手机处理能力。

- 海量的库支持，更快实现
Python 世界中积累了多年的大部分的类库都能够被快速引入到 QPython 体系中，因此您可以不必重复造轮子。

- 最小的开发环境要求
进行 QPython 开发，您只需要有一台安卓手机即可。当然您也可以在 PC 端完成开发，再将程序上传到 QPython 上；现在QPython已经推出了一个QWE(QPython Web Editor)工具，更能让你只需要通过一个浏览器就可以连接你的手机进行开发。



项目“公交线路查询”简介
---
设计一个“公交线路查询”的QPython WebApp应用，主要以html作为UI，使用Python来调用Android系统的接口。
该应用有两个应用界面，一个用以收集用户输入的关键词（如需要查询的公交线路、始发地、目的地等），然后传递到另外一个应用界面里，让这个应用界面去以此作为参数去请求爱帮公交查询API，并将返回的JSON格式数据处理后展现到界面上。


公交线路查询功能，如图1-1所示。



换乘查询功能，如图1-2所示。



案例设计与实现
---------

### 需求分析

#### 项目实现的功能:

实现“公交路线查询”和“换乘查询”功能。这两个功能的实现方法实则上是大同小异的。爱帮公交提供给了开发者公交“线路查询”和“换乘查询”的API，我们只需将用户输入的关键词作为参数去请求对应API，即可取得用户所期望的数据，再将这些数据解析并展现到界面。故不涉及复杂的算法问题和本地数据库操作。

主界面中能自动定位用户的所在城市，即自动帮助用户判断所在的城市，并自动为用户填充“城市名”输入框。实现方法为获取当前联网用户的外网IP，通过请求百度IP定位API得到用户的城市名。

可以用Python开发的模式创建一个Web工程，工程目录结构如图1-3所示


### 界面设计

由于本次项目使用QPython WebApp作为主要框架，所以只需创建一个主布局文件，并添加一个填充父元素的WebView控件，每个Activity都加载这个布局文件，再将html页面加载到WebView控件中。本项目的html页面较为简单，故无需使用专门的IDE去编写代码，可直接选用自己所喜好的文本编辑器即可。主布局文件代码如图1-4所示



之后，使用html设计APP的主界面，“线路查询”模块，主要有两个输入框，分别收集用户的“城市”和所要查询的“公交线路”。还要有一个“查询”按钮。为了使得用户界面更加美观，这里使用了Amaze UI这个前端框架（官方网站：http://amazeui.org/），并将核心文件（框架的js、css文件，html文件等）放置在项目的assets文件夹中，目录结构如图1-5所示。


在html中，可以使用<link>标签引用assets中的css，js等文件，href属性使用file:///android_asset/ 定位到assets目录下。如图1-6所示。引用其他本地资源时可类比。


上面说过，html页面是被加载到WebView控件里来作为软件UI的，所以我们首先要使用html语言来编写界面。已经知道了html、css、js等文件在工程目录assets中是如何放置后，就可以开始设计软件的主界面了。

主界面index.html设计要点：
1、框架文件的引入。使用link标签在head、body体中引入必要的css和js文件。
2、参照AmazeUI的官方文档，根据需求去引用框架已经定义好的美观的网页控件元素。引用到的组件如图1-7所示，代码可参照文档和源码。


3、定义JavaScript函数供逻辑代码调用。之前说过，主界面实现的逻辑有二，一为根据用户的IP获取用户所在城市，然后改变html页面上的“所在地”输入框和底部高亮提示字，而后者操作需要利用JavaScript对Dom进行操作，故定义setCity函数，以参数去替换html中的内容。二是“查询按钮”被点击时，需要将表单的值通过函数调用的方式，传递给逻辑代码进行Activity跳转和数据请求等操作，细节部分下面会讲到。定义为btnOnclick函数，并将该函数绑定到“查询按钮”的OnClick事件中。

主界面index.html的代码如下。


查询结果展现页面detail.html，设计要点：
1、使用到AmazeUI的折叠菜单控件展现查询结果，具体代码请参照AmazeUI的官方文档和源码。
2、定义结果项插入相关JavaScript函数。定义appendDetail函数，用以将API返回的数据通过固定的格式添加到html节点中。定义resultCount函数，用以将返回结果条数显示到导航栏上。

查询结果展现页面detail.html代码如下：


### 功能实现

以下以主界面MainActivity为例，说明html与Java如何通过JavaScript实现数据的传递。MainActivity主要加载index.html到WebView作为UI，也是以下第一点介绍的。第二点主要讲解如何定义html与Java交互的方法。例如主界面加载后，需要通过JAVA代码获取到用户所在地，通过JavaScript加载到html上，还有用户点击html上的“查询按钮”时，通过JavaScript将数据传递到JAVA代码中并执行Activity跳转操作。

#### 初始化WebView控件


MainActivity.java为主界面的Activity，而index.html是我们设计的主界面UI，所以要通过WebView组件，将index.html加载到MainActivity。如图1-8所示，为该Activity的onCreate方法的实现。


由代码可知，我们先加载一个主布局文件作为当前Activity的布局，此布局文件即为2.2“界面设计”中提及的，只包含WebView一个控件的xml布局文件。然后新建一个线程类，作http请求。最后再实例化WebView对象，并调用该对象的相关方法，设置了WebView的一系列参数。主要是进行隐藏WebView控件原有的缩放按钮，打开对JavaScript的支持等参数设置等，使得WebView中的html能填充整个布局，更像Android的原生界面。


#### 定义html与Java交互的方法


图2-3-1-1中的webview.addJavascriptInterface(this, "android")语句，作用是设置接口，也是打通html与JAVA的数据传递通道的关键，使得html中的JavaScript方法能通过“window.android.方法名”调用Java中的方法，Java中通过webview的loadUrl方法可以调用html中的JavaScript方法。官方文档截图如图1-9所示。
注意：需在本类或onCreate方法添加注解@SuppressLint("JavascriptInterface")，和导入android.annotation.SuppressLint包，不然方法调用时会报错：找不到方法。并且被@JavascriptInterface注解的公有方法才能在webview中被调用。


##### 通过JavaScript调用Java方法

在MainActivity中定义callDetailActivity方法，用于绑定到html中的Button标签的OnClick事件，实现点击按钮后，完成检查网络连接状态、传递数据并跳转到新的Activity的功能。callDetailActivity方法代码如图1-10

Index.html中，可以通过JavaScript语句window.android.callDetailActivity(city, keyword)调用MainActivity中相应的callDetailActivity方法。html代码如图1-11所示，实现了点击button后，将id为city和keyword的两个input标签中的value属性值作为参数调用图1-10的callDetailActivity方法。（注：图1-11、图1-12为文本编辑器NotePad2的截图）


##### 通过Java调用JavaScript的方法

在index.html的Script标签中定义一个方法，作用是把 “所在城市”（参数）填充到id为city的input标签和id为message的span标签中。如图1-12所示


还需要在MainActivity中定义一个类继承自WebViewClient类，可重写类内的onPageStarte, onPageFinished,shouldOverrideUrlLoading方法。定义WebView控件加载html开始时、完成后执行的操作。重写shouldOverrideUrlLoading方法，使点击链接后不使用其他的浏览器打开。代码如图1-13所示



上图中，页面加载成功后，通过调用webView的loadUrl方法执行在index.html中定义的setCity方法，并将在Java中请求API获得的城市名作为参数传递过去。实现的逻辑是，用户在启动软件后，在后台请求API获取到用户的所在城市，然后在WebView加载html页面，当页面加载完成后，最后调用setCity方法。


### 向API请求数据

对于请求数据这部分和数据处理这部分，可将逻辑代码封装到一个类中。通过HttpClient等类进行POST或GET请求，返回的JSON数据使用JSONObject或JSONArray类进行处理，提取到需要的信息。需要注意的是，http请求属于耗时操作，在UI线程内，即在onCreate内直接执行请求的话程序会抛出Exceptin。故需要创建新的线程类执行http请求，数据处理完成后再通过Handler对象进行传递，更新UI控件等操作。由于这部分不是讨论重点，故只是概括一下实现逻辑，实现方法详见源码。

至此，以MainActivity为例，介绍了将html页面用作Android UI的方法。其他Activity中方法雷同，Activity的大体结构如图所示1-14，我们只需根据不同的需求，更改相应的代码块即可。具体实现方法请参照源码。


项目心得
-----
成熟的web前端框架使得构建界面风格友好的html变得简单，使用html作为Android UI，不但可以节省开发者设计原生UI所要花费的时间，而且更新迅速、紧随UI发展潮流的web前端UI框架能很大程度增加用户的体验。

谈及缺点，由该项目可知，简单的文本数据传递是可以做到的。但是若要使得html元素与手机硬件模块，如蓝牙、陀螺仪、摄像头等交互的话，可能比较难处理。其实亦有软件厂商提供解决方案，如APICloud、HBuilder、PhoneGap等，旨在使用HTML5开发出原生体验的APP，但是如果要到这种解决方案，需要用到它提供的一套规范去编码，甚至需要用到它们提供的IDE，无疑这又是另外一种局限性。并且移动设备的硬件水平的不同，也会导致效率问题的产生。



参考资料
-----

项目源码：
https://github.com/cyn8/-BusHelper

百度IP定位API文档：
http://developer.baidu.com/map/index.php?title=webapi/ip-api

爱帮公交线路查询API文档：
http://www.aibang.com/api/usage#bus_lines

AmazeUI前端框架官方网站：
http://amazeui.org/

常见问题
-------

### 处理html加载时白屏的另类方法

虽然html文件在本地，但是该项目的Activity处理逻辑是等待请求API、数据解释完成后才完整加载html页面的，所以会受到网络因素的制约，可能会出现html加载时白屏的问题，因而造成不友好的用户体验。
解决方法：
在OnCreate方法执行时，先实例化安卓的ProgressDialog控件，显示加载圈，并有相关提示性文字，待耗时操作完成和html加载完成后，再执行ProgressDialog对象的dismiss()方法，将该控件隐藏掉。html加载时效果如图1-15所示。


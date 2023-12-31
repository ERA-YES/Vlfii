# Vlfii
小鸟飞飞图形化编程的文本编程，针对于小鸟飞飞图形化编程群控软件，采用python构建，可直接引用为库运行，目前已实现大部分常用函数，快比赛了，大概会断更

### 在博客里体验效果更佳哦
**[博客链接](https://blog.erayes.top/2023/07/18/vlfii/)**

### 使用注意
建议将库文件与源代码文件放在同一目录下

使用前设置无人机列表、文件名、音乐名等:
```python
from vlfii import *
import vlfii

#默认ip从"192.168.31.101"递增，传入第三参数以调整
vlfii.DRONE = [
    [x1, y1, ["192.169.31.109"]],
    [x2, y2],
    [x3, y3],
    [x4, y4],
    [x5, y5],
]
vlfii.FILE = "output"
vlfii.TEST = False

music("好听的音乐")
```
所有代码写完后:
```python
save()
```
最后运行程序，在程序同一目录下就会生成"output.vlfii"

**注意，在使用群控软件打开后，需要一次点击飞机以让程序生成文本代码，否则将会报错**

**我之所以没实现这部分的逻辑就是因为没有这些代码程序能照常打开，而且软件能自动生成**

### 下表为图形化代码块与函数的对于关系
|代码块|函数|参数|说明|返回值|
|---|---|---|---|---|
|开始|start|-|-|-|
|Start at|StartTime|time = "00:00", color = "#cccccc"|-|-|
|结束Start at代码块|End|-|-|-|
|延时|Delay|time = 1000|-|-|
|解锁|Unlock|-|-|-|
|上锁|Lock|-|-|-|
|水平速度 水平加速度|Horizontal|hSpeed = 100, hAcc = 100|-|-|
|垂直速度 垂直加速度|Vertical|vSpeed = 100, vAcc = 100|-|-|
|角速度|AngularVelocity|w|-|-|
|起飞  cm|TakeOff|alt = 120|-|-|
|降落|Land|-|-|-|
|直线移至|MoveToCoord|x, y, z = 120|-|-|
|X, Y, Z方向移动|RelativePosition|x, y, z|-|-|
|飞机灯光变为|LedAllOn|color="#ffffff"|-|-|
|熄灭飞机灯光|LedAllOff|-|-|-|
|飞机在delay毫秒内逐渐变为color，亮度为bright，然后dur毫秒内变暗|LedAllBreath|color, delay = 1000, dur = 1000, bright = 1|-|-|
|机身在delay毫秒内逐渐变为color，亮度为bright，然后dur毫秒内变暗|LedBodyBreath|color, delay = 1000, dur = 1000, bright = 1|-|-|
|机身灯光先变为color，亮度为bright，持续dur,再关闭delay|LedBodyBlink|color, dur, delay, bright|-|-|
|机身灯光变为|LedBodyOn|color="#ffffff"|-|-|
|直线移至，飞机灯光变为|WaypointRGB|x, y, z, color|-|-|
|四个机臂灯光变为color1, color2, color3, color4, 然后灯光True/False时针方向旋转，转一圈时间为delay|LedDroneArmHorse|color1, color2, color3, color4, clock, delay|-|-|
|四个机臂同亮脉冲color1, color2, color3, color4，频率frequency|LedDroneArmPulse|color1, color2, color3, color4, frequency|-|-|
|结束一架飞机并转向下一架|finish|-|-|-|

### 新增功能
|函数|参数|说明|返回值|
|---|---|---|---|
|Start|-|`start`的别名，用于转换|-|
|Arm|-|`Unlock`的别名，用于转换
|Takeoff|-|`TakeOff`的别名，用于转换|-|
|Move|-|`Move`的别名，用于转换|-|
|MoveToCoord_AutoDelay|x, y, z = 120, time = 0|传入目标坐标，增减时间, 或传入百分比"xx%"|int 时间|
|Move_Circle|x, y, z = 120, n = 8, r = 100, time = 0|飞圆心为传入坐标的n个点的半径为r的圆|int tot 总时间|
|Move_CircleFind|A, B, z = 120, n = 16, dir = 1, time = 0|直接从B点开始飞圆心为A点的圆|int tot 总时间|
|Circle|n, r, dir = 1|返回一个被n均分的圆|list c|
|Circle_FindPoint|A, B, n, dir = 1|返回圆心A点，B点开始向dir方向的圆|list p|
|music|name|设定代码的音乐，接受文件名|-|
|Time|output|计算以返回当前时间, output为True时输出当前时间|str "MM:SS"|
|Vprint|s|以当前无人机发言|输出"{ip} saying: {s}"|-|

**函数介绍较简单，更多请在代码里查看**

### 转换器
**VlfiiConverter**
> 复制`小鸟飞飞图形化编程群控软件`右侧生成的文本源代码，运行`VlfiiConverter.py`，程序将会直接输出转换后的python程序，此程序在引用本Vlfii库是，可以直接运行并生成代码。
- 在安装`pyperclip`库后程序将直接将转换后的代码粘贴入剪贴板

命令行运行此程序以安装`pyperclip`库
```
pip install pyperclip
```

**!注意，生成的代码在`from Vlfii import *`时才有效**

### 库内部变量
|变量名|属性|值|功能|
|---|---|---|---|
|__STATEMENT|私有值|-|表示当前状态|
|__FATHER|私有值|-|表示父标签|
|__WEB_XML|私有值|-|表示WebXml标签|
|__XML|私有值|-|表示Xml标签|
|__hSpeed|私有值|-|记录当前无人机的水平速度|
|__hAcc|私有值|-|记录当前无人机的水平加速度|
|DRONE_NUM|列表|-|当前代码框的无人机编号|
|TIME|公共|整型|记录当前时间|
|FILE|公共|字符串|输出文件名|
|POS|公共|列表|飞机当前坐标|
|DRONE|公共|列表|无人机列表|
|IP|公共|列表|无人机IP列表|
|TEST|公共|布尔值|调试模式开关，开启时生成文件不可用|

### 颜色变量
|变量名|值|颜色|
|blue|"#33ccff"|蓝色<div style="background-color: #33ccff; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|yellow|"#ffff00"|黄色<div style="background-color: #ffff00; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|orange|"#ff6600"|橙色<div style="background-color: #ff6600; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|grey|"#c0c0c0"|灰色<div style="background-color: #c0c0c0; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|red|"#ff0000"|红色<div style="background-color: #ff0000; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|white_red|"#ffcccc"|浅红色<div style="background-color: #ffcccc; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|green|"#33cc00"|绿色<div style="background-color: #33cc00; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|white_yellow|"#ffffcc"|淡黄色<div style="background-color: #ffffcc; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|
|white|"#ffffff"|白色<div style="background-color: #ffffff; border: 1px solid white; border-radius: 4px; width: 12px; height: 12px; display: inline-block;"></div>|

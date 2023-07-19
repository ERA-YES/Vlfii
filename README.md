# Vlfii
小鸟飞飞图形化编程的文本编程，针对于小鸟飞飞图形化编程群控软件，采用python构建，可直接引用为库运行，目前已实现大部分常用函数，正在更新中

### 在博客里体验效果更佳哦
**[博客链接](https://erayes.top/2023/07/18/vlfii/)**

### 下表为图形化代码块与函数的对于关系
|代码块|函数|参数|说明|返回值|
|---|---|---|---|---|
|开始|start()|-|-|-|
|Start at|StartTime()|time = "00:00", color = "#cccccc"|-|-|
|结束Start at代码块|End()|-|-|-|
|延时|Delay()|time = 1000|-|-|
|解锁|Unlock()|-|-|-|
|上锁|Lock()|-|-|-|
|水平速度 水平加速度|Horizontal()|hSpeed = 100, hAcc = 100|-|-|
|垂直速度 垂直加速度|Vertical()|vSpeed = 100, vAcc = 100|-|-|
|起飞  cm|TakeOff()|alt = 120|-|-|
|降落|Land()|-|-|-|
|直线移至|MoveToCoord()|x, y, z = 120|-|-|
|飞机灯光变为|LedAllOn()|color="#ffffff"|-|-|
|机身灯光变为|LedBodyOn()|color="#ffffff"|-|-|
|结束一架飞机并转向下一架|finish()|-|-|-|

### 新增功能
|函数|参数|说明|返回值|
|---|---|---|---|
|MoveToCoord_AutoDelay|x, y, z = 120, time = 0|传入目标坐标，增减时间|距离|
|Move_Circle|x, y, z = 120, n = 8, r = 100, d = 1400|飞圆心为传入坐标，以d的deplay为间隔的n个点的半径为r的圆|-|
|Move_Circle_AutoDeplay|x, y, z = 120, n = 8, r = 100, time = 0|整合以上两个功能|-|


### 库内部变量
|变量名|属性|值|功能|
|---|---|---|---|
|__STATEMENT|私有值|-|表示当前状态|
|__FATHER|私有值|-|表示父标签|
|__WEB_XML|私有值|-|表示WebXml标签|
|__XML|私有值|-|表示Xml标签|
|__DRONE_NUM|私有值|-|当前代码框的无人机编号|
|FILE|公共|字符串|输出文件名|
|POS|公共|列表|飞机当前坐标|
|DRONE|公共|列表|无人机列表|
|TEST|公共|布尔值|调试模式开关，开启时生成文件不可用|

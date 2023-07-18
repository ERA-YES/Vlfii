# Vlfii
小鸟飞飞图形化编程的文本编程，针对于小鸟飞飞图形化编程群控软件，采用python构建，可直接引用为库运行，目前已实现大部分常用函数，正在更新中

### 下表为图形化代码块与函数的对于关系
|代码块|函数|参数|
|---|---|---|
|开始|start()|-|
|Start at|StartTime()|time = "00:00", color = "#cccccc"|
|结束Start at代码块|End()|-|
|延时|Delay()|time = 1000|
|解锁|Unlock()|-|
|上锁|Lock()|-|
|水平速度 水平加速度|Horizontal()|hSpeed = 100, hAcc = 100|
|垂直速度 垂直加速度|Vertical()|vSpeed = 100, vAcc = 100|
|起飞  cm|TakeOff()|alt = 120|
|降落|Land()|-|
|直线移至|MoveToCoord()|x, y, z = 120|
|飞机灯光变为|LedAllOn()|color="#ffffff"|
|机身灯光变为|LedBodyOn()|color="#ffffff"|
|结束一架飞机并转向下一架|finish()|-|

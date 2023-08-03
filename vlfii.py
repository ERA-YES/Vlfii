import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import math
from datetime import timedelta
from datetime import datetime

#region all
__STATEMENT = None
__FATHER = None
__WEBXML = None
__XML = None
__DRONE_NUM = 0
__hSpeed = 100
__hAcc = 200
TIME = 0
FILE = "output"
POS = [0, 0, 0]
DRONE = []
TEST = False

blue = "#33ccff"
yellow = "#ffff00"
orange = "#ff6600"
grey = "#c0c0c0"

#region Setups

root = ET.Element("FiiConfig", {"xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
                                "xmlns:xsd": "http://www.w3.org/2001/XMLSchema"})

FlightType = ET.SubElement(root, "FlightType")
FlightType.text = "F700"

CommunicationMode = ET.SubElement(root, "CommunicationMode")
CommunicationMode.text = "Qr"

ComName = ET.SubElement(root, "ComName")

MapInfo = ET.SubElement(root, "MapInfo")
Width = ET.SubElement(MapInfo, "Width")
Width.text = "400"
Height = ET.SubElement(MapInfo, "Height")
Height.text = "400"

MusicInfo = ET.SubElement(root, "MusicInfo")
Name = ET.SubElement(MusicInfo, "Name")
Format = ET.SubElement(MusicInfo, "Format")
Format.text = "mp3"

Flights = ET.SubElement(root, "Flights")

#endregion

def music(name):
    """设置音乐

    Args:
        name (str): 音乐文件名
    """
    Name.text = name

def start():
    """开始一架飞机
    """
    global __FATHER, __XML, __WEBXML, DRONE, POS
    i = __DRONE_NUM
    FlightView = ET.SubElement(Flights, "FlightView")
    Ip = ET.SubElement(FlightView, "Ip")
    try:
        Ip.text = DRONE[i][2]
    except IndexError:
        Ip.text = "192.168.31.10{}".format(i+1)
    InitPos = ET.SubElement(FlightView, "InitPos")
    X = ET.SubElement(InitPos, "X")
    X.text = str(DRONE[i][0])
    Y = ET.SubElement(InitPos, "Y")
    Y.text = str(DRONE[i][1])
    POS = [*DRONE[i], 0]
    Code = ET.SubElement(FlightView, "Code")
    __WEBXML = ET.SubElement(FlightView, "WebXml")
    __XML = ET.SubElement(__WEBXML, "xml", {"xmlns":"https://developers.google.com/blockly/xml"})
    block = ET.SubElement(__XML, "block", {"type":"Goertek_Start", "x":"300", "y":"100"})
    __FATHER = block

def Time():
    """转换时间

    Returns:
        str: "MM:SS"时间格式
    """
    s = math.ceil(TIME / 1000)
    return f"{datetime(1900, 1, 1, 0, 0, 0) + timedelta(seconds=s) % timedelta(minutes=60):%M:%S}"

def _next():
    global __FATHER
    next = ET.SubElement(__FATHER, "next")
    __FATHER = next

def _type(t):
    return {"type":"Goertek_"+t}

def _name(n):
    return {"name":n}

def _field(b, n, t):
    field = ET.SubElement(b, "field", _name(n))
    field.text = str(t)

def _block(n):
    global __FATHER
    if __FATHER.tag != "next" and __FATHER.tag != "statement":
        _next()
    b = ET.SubElement(__FATHER, "block", _type(n))
    __FATHER = b
    return b

def StartTime(time = "auto", color = "#cccccc"):
    """开始"StartTime"代码块

    Args:
        time (str, optional): 时间. Defaults to "auto".
        color (str, optional): 颜色. Defaults to "#cccccc".
    """
    global __FATHER, __STATEMENT
    b = _block("StartTime")
    _field(b, "time", Time() if time == "auto" else time)
    _field(b, "color", color)
    statement = ET.SubElement(b, "statement", _name("functionIntit"))
    __STATEMENT = b
    __FATHER = statement

def End():
    """结束"StartTime"代码块
    """
    global __FATHER
    next = ET.SubElement(__STATEMENT, "next")
    __FATHER = next

def UnLock():
    """解锁
    """
    global __FATHER
    b = ET.SubElement(__FATHER, "block", _type("UnLock"))
    __FATHER = b

def Lock():
    """上锁
    """
    _block("Lock")

def Delay(time = 1000):
    """延时

    Args:
        time (int, optional): 时间. Defaults to 1000.
    """
    global TIME
    b = _block("Delay")
    _field(b, "delay", 0)
    _field(b, "time", time)
    TIME += time

def Horizontal(hSpeed = 100, hAcc = 100):
    """水平速度和加速度

    Args:
        hSpeed (int, optional): 水平速度. Defaults to 100.
        hAcc (int, optional): 水平加速度. Defaults to 100.
    """
    global __hAcc, __hSpeed
    b = _block("Horizontal")
    _field(b, "hSpeed", hSpeed)
    _field(b, "hAcc", hAcc)
    __hSpeed = hSpeed
    __hAcc = hAcc

def Vertical(vSpeed = 100, vAcc = 100):
    """垂直速度和加速度

    Args:
        vSpeed (int, optional): 垂直速度. Defaults to 100.
        vAcc (int, optional): 垂直加速度. Defaults to 100.
    """
    b = _block("Vertical")
    _field(b, "vSpeed", vSpeed)
    _field(b, "vAcc", vAcc)

def AngularVelocity(w):
    """角速度

    Args:
        w (int): °/s
    """ 
    b = _block("AngularVelocity")
    _field(b, "w", w)

def TakeOff(alt=120):
    """起飞

    Args:
        alt (int, optional): 高度. Defaults to 120.
    """
    global POS
    b = _block("TakeOff")
    _field(b, "alt", alt)
    POS[2] = alt

def Land():
    """降落
    """
    b = _block("Land")

def RelativePosition(x, y, z):
    """相对位置移动

    Args:
        x (int): x轴移动距离
        y (int): y轴移动距离
        z (int): z轴移动距离
    """
    global POS
    b = _block("Move")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)
    POS[0] += x
    POS[1] += y
    POS[2] += z

def MoveToCoord(x, y, z = 120):
    """直线移至

    Args:
        x (int): 目标位置x
        y (int): 目标位置y
        z (int, optional): 目标位置z. Defaults to 120.
    """
    global POS
    b = _block("MoveToCoord")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)
    POS = [x, y, z]

def MoveToCoord_AutoDelay(x, y, z = 120, time = 0):
    """直线移至并自动延时

    Args:
        x (int): 目标位置x
        y (int): 目标位置y
        z (int, optional): 目标位置z. Defaults to 120.
        time (int, optional): 增减延时. Defaults to 0.

    Returns:
        int, int: 总延时, 移动距离
    """
    global POS, TIME
    b = _block("MoveToCoord")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)
    v = __hSpeed
    a = __hAcc
    d = math.sqrt((x - POS[0])**2 + (y - POS[1])**2 + (z - POS[2])**2)
    t = v / a
    D = (v**2) / (2 * a)
    if d > 2 * D:
        T = 2 * t + (d - 2 * D) / v
    else:
        T = 2 * math.sqrt(d / a)
    T = round(T * 1000) + time
    Delay(T)
    TIME += T
    POS = [x, y, z]
    return T, d

def Circle(n, r, dir = 1):
    """生成圆

    Args:
        n (int): 平分成n份
        r (int): 半径
        dir (int, optional): 方向(1/-1). Defaults to 1.

    Returns:
        list: 圆列表
    """
    c = []
    angle = dir * 2 * math.pi / n
    for i in range(n):
        theta = i * angle
        c.append([round(r * math.cos(theta)), 
                  round(r * math.sin(theta))])
    c.append([round(r), 0])
    return c

def Circle_FindPoint(A, B, n, dir = 1):
    """找到圆

    Args:
        A (list): 圆心坐标[x, y]
        B (list): 寻找点坐标[x, y]
        n (int): 平分成n份
        dir (int, optional): 方向(1/-1). Defaults to 1.
    """
    def distance(A, B):
        return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
    r = math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
    c = [[i[0] + A[0], i[1] + A[1]] for i in Circle(n, r, dir)]
    # c = Circle(n, r, dir)
    j = [i for i in c if distance(i ,B) == min(distance(i, B) for i in c)][0]
    p = []
    for i in range(len(c)):
        if c[i] == j:
            p = c[i + 1:] + c[:i + 1]
            return p

def Move_Circle(x, y, z = 120, n = 8, r = 100, dir = 1, time = 0):
    """移动一个圆

    Args:
        x (int): 圆心位置x
        y (int): 圆心位置y
        z (int, optional): 圆心位置z. Defaults to 120.
        n (int, optional): 平分成n份. Defaults to 8.
        r (int, optional): 半径. Defaults to 100.
        dir (int, optional): 方向(1/-1). Defaults to 1.
        time (int, optional): 增减延时. Defaults to 0.

    Returns:
        int: 总延时
    """
    global TIME
    tot = 0
    for [dx, dy] in Circle(n, r, dir):
        tot += MoveToCoord_AutoDelay(x + dx, y + dy, z, time)[0]
    TIME += tot
    return tot

def Move_CircleFind(A, B, z = 120, n = 16, dir = 1, time = 0):
    """找到圆并移动

    Args:
        A (list): 圆心坐标[x, y]
        B (list): 寻找点坐标[x, y]
        z (int, optional): 高度. Defaults to 120.
        n (int, optional): 平分成n份. Defaults to 16.
        dir (int, optional): 方向(1/-1). Defaults to 1.
        time (int, optional): 增减延时. Defaults to 0.

    Returns:
        int: 总延时
    """
    global TIME
    tot = 0
    for [dx, dy] in Circle_FindPoint(A, B, n, dir):
        # tot += MoveToCoord_AutoDelay(A[0] + dx, A[1] + dy, z, time)[0]
        tot += MoveToCoord_AutoDelay(dx, dy, z, time)[0]
    TIME += tot
    return tot

def LedAllOn(color="#ffffff"):
    """飞机灯光变为

    Args:
        color (str, optional): 颜色. Defaults to "#ffffff".
    """
    b = _block("LedAllOn")
    _field(b, "color", color)

def WaypointRGB(x, y, z, color):
    """直线移至，飞机灯光变为

    Args:
        x (int): 目标位置x
        y (int): 目标位置y
        z (int): 目标位置z
        color (str): 颜色
    """
    MoveToCoord(x, y, z)
    LedAllOn(color)

def LedAllOff():
    """熄灭飞机灯光
    """
    _block("LedAllOff")

def LedBodyOn(color="#ffffff"):
    """机身灯光变为

    Args:
        color (str, optional): 颜色. Defaults to "#ffffff".
    """
    b = _block("LedBodyOn")
    _field(b, "color", color)

def LedAllBreath(color, delay = 1000, dur = 1000, bright = 1):
    """飞机灯光呼吸

    Args:
        color (str): 颜色
        delay (int, optional): 在delay毫秒内逐渐变色. Defaults to 1000.
        dur (int, optional): 在dur毫秒内变暗. Defaults to 1000.
        bright (int, optional): 亮度为bright(0~1). Defaults to 1.
    """
    b = _block("LedAllBreath")
    _field(b, "dur", dur)
    _field(b, "color", color)
    _field(b, "bright", bright)
    _field(b, "delay", delay)

def LedBodyBreath(color, delay = 1000, dur = 1000, bright = 1):
    """飞机机身灯光呼吸

    Args:
        color (str): 颜色
        delay (int, optional): 在delay毫秒内逐渐变色. Defaults to 1000.
        dur (int, optional): 在dur毫秒内变暗. Defaults to 1000.
        bright (int, optional): 亮度为bright(0~1). Defaults to 1.
    """
    b = _block("LedBodyBreath")
    _field(b, "dur", dur)
    _field(b, "color", color)
    _field(b, "bright", bright)
    _field(b, "delay", delay)

def LedBodyBlink(color, dur, delay, bright):
    """飞机机身灯光持续

    Args:
        color (str): 颜色
        dur (int): 持续dur毫秒
        delay (int): delay毫秒后关闭
        bright (int): 亮度为bright(0~1)
    """
    b = _block("LedBodyBlink")
    _field(b, "color", color)
    _field(b, "birght", bright)
    _field(b, "dur", dur)
    _field(b, "delay", delay)

def LedDroneArmHorse(color1, color2, color3, color4, clock, delay):
    """四个机臂灯光变为

    Args:
        color1 (str): 颜色1
        color2 (str): 颜色2
        color3 (str): 颜色3
        color4 (str): 颜色4
        clock (bool): 顺/逆时针(True/False)
        delay (int): 转一圈时间为delay毫秒
    """
    b = _block("LedDroneArmHorse")
    _field(b, "color1", color1)
    _field(b, "color2", color2)
    _field(b, "color3", color3)
    _field(b, "color4", color4)
    _field(b, "clock", clock)
    _field(b, "delay", delay)

def LedDroneArmPulse(color1, color2, color3, color4, frequency):
    """四个机臂同亮脉冲

    Args:
        color1 (str): 颜色1
        color2 (str): 颜色2
        color3 (str): 颜色3
        color4 (str): 颜色4
        frequency (int): 频率
    """
    b = _block("LedDroneArmPulse")
    _field(b, "color1", color1)
    _field(b, "color2", color2)
    _field(b, "color3", color3)
    _field(b, "color4", color4)
    _field(b, "frequency", frequency)

def finish():
    """结束这架飞机
    """
    global __DRONE_NUM
    if not TEST:
        str_xml = str(ET.tostring(__XML, encoding='utf-8', method="xml"))
        __WEBXML.clear()
        __WEBXML.text = str_xml[2: (len(str_xml) - 1)]
    __DRONE_NUM += 1

def save():
    """生成代码
    """
    rough_str = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_str)
    new_str = reparsed.toprettyxml(indent='  ')
    f = open('{}.vlfii'.format(FILE), 'w', encoding='utf-8')
    f.write(new_str)
    f.close()

Move = MoveToCoord
Takeoff = TakeOff
Disarm = Lock
Arm = UnLock
Start = start

#endregion all

if __name__ == "__main__":
    DRONE = [
        [160, 160],
        [1, 1],
        [2, 2],
        [3, 3]
    ]
    start()
    StartTime()
    UnLock()
    Delay()
    Horizontal()
    Vertical()
    TakeOff()
    Delay(3000)

    MoveToCoord_AutoDelay(260, 260, time=700)
    Move_CircleFind([160, 160], POS[:2])

    Delay(1000)
    Land()
    Delay(1000)
    Lock()
    finish()
    save()
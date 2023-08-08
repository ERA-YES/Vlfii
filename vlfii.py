import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import math

#region all
__STATEMENT = None
__FATHER = None
__WEBXML = None
__XML = None
__hSpeed = 100
__hAcc = 200
DRONE_NUM = 0
TIME = 0
FILE = "output"
POS = [0, 0, 0]
DRONE = []
IP = []
TEST = False

blue = "#33ccff"
yellow = "#ffff00"
orange = "#ff6600"
grey = "#c0c0c0"
red = "#ff0000"
white_red = "#ffcccc"
green = "#33cc00"
white_yellow = "#ffffcc"
white = "#ffffff"

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

def Vprint(s):
    print("\033[31m" + IP[DRONE_NUM] + " saying: \033[32m" + s + "\033[37m")

def music(name):
    """====================\n
    设置音乐

    ====================\n
    参数:
        name (str): 音乐文件名\n
    """
    Name.text = name

def start():
    """====================\n
    开始一架飞机
    """
    global __FATHER, __XML, __WEBXML, DRONE, POS, IP
    i = DRONE_NUM
    FlightView = ET.SubElement(Flights, "FlightView")
    Ip = ET.SubElement(FlightView, "Ip")
    try:
        Ip.text = DRONE[i][2]
        IP.append(DRONE[i][2])
    except IndexError:
        Ip.text = "192.168.31.10{}".format(i+1)
        IP.append("192.168.31.10{}".format(i+1))
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
    Vprint("Started!")

def Time(output = False):
    """====================\n
    转换时间

    Returns:
        str: "MM:SS"时间格式
    """
    s = f"{TIME // 60000 :02d}:{math.ceil(TIME / 1000) % 60 :02d}"
    Vprint("Now Time: " + s) if output else None
    return s

def StartTime(time = "auto", color = "#cccccc"):
    """====================\n
    开始'StartTime'代码块

    ====================\n
    参数:
        time (str, 可选): 时间。默认值为： "auto".\n
        color (str, 可选): 颜色。默认值为： "#cccccc".\n
    """
    global __FATHER, __STATEMENT, TIME
    b = _block("StartTime")
    if time == "auto":
        _field(b, "time", Time())
    else:
        _field(b, "time", time)
        minutes, seconds = time.split(':')
        TIME = (int(minutes) * 60 + int(seconds)) * 1000
    _field(b, "color", color)
    statement = ET.SubElement(b, "statement", _name("functionIntit"))
    __STATEMENT = b
    __FATHER = statement

def End():
    """====================\n
    结束"StartTime"代码块
    """
    global __FATHER
    next = ET.SubElement(__STATEMENT, "next")
    __FATHER = next

def UnLock():
    """====================\n
    解锁
    """
    global __FATHER
    b = ET.SubElement(__FATHER, "block", _type("UnLock"))
    __FATHER = b

def Lock():
    """====================\n
    上锁
    """
    _block("Lock")

def Delay(time = 1000):
    """====================\n
    延时

    ====================\n
    参数:
        time (int, 可选): 时间。默认值为： 1000.\n
    """
    global TIME
    b = _block("Delay")
    _field(b, "delay", 0)
    _field(b, "time", time)
    TIME += time

def Horizontal(hSpeed = 100, hAcc = 100):
    """====================\n
    水平速度和加速度

    ====================\n
    参数:
        hSpeed (int, 可选): 水平速度。默认值为： 100.\n
        hAcc (int, 可选): 水平加速度。默认值为： 100.\n
    """
    global __hAcc, __hSpeed
    b = _block("Horizontal")
    _field(b, "hSpeed", hSpeed)
    _field(b, "hAcc", hAcc)
    __hSpeed = hSpeed
    __hAcc = hAcc

def Vertical(vSpeed = 100, vAcc = 100):
    """====================\n
    垂直速度和加速度

    ====================\n
    参数:
        vSpeed (int, 可选): 垂直速度。默认值为： 100.\n
        vAcc (int, 可选): 垂直加速度。默认值为： 100.\n
    """
    b = _block("Vertical")
    _field(b, "vSpeed", vSpeed)
    _field(b, "vAcc", vAcc)

def AngularVelocity(w):
    """====================\n
    角速度

    ====================\n
    参数:
        w (int): °/s\n
    """ 
    b = _block("AngularVelocity")
    _field(b, "w", w)

def TakeOff(alt=120):
    """====================\n
    起飞

    ====================\n
    参数:
        alt (int, 可选): 高度。默认值为： 120.\n
    """
    global POS
    b = _block("TakeOff")
    _field(b, "alt", alt)
    POS[2] = alt

def Land():
    """====================\n
    降落
    """
    b = _block("Land")

def RelativePosition(x, y, z):
    """====================\n
    相对位置移动

    ====================\n
    参数:
        x (int): \n
        y (int): y轴移动距离\n
        z (int): z轴移动距离\n
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
    """====================\n
    直线移至

    ====================\n
    参数:
        x (int): 目标位置x\n
        y (int): 目标位置y\n
        z (int, 可选): 目标位置z。默认值为： 120.\n
    """
    global POS
    b = _block("MoveToCoord")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)
    POS = [x, y, z]

def MoveToCoord_AutoDelay(x, y, z = 120, time = 0):
    """====================\n
    直线移至并自动延时

    ====================\n
    参数:
        x (int): 目标位置x\n
        y (int): 目标位置y\n
        z (int, 可选): 目标位置z。默认值为： 120.\n
        time (int/str, 可选): 增减延时。默认值为： 0.\n

    Returns:
        int, float: 总延时, 移动距离
    """
    global POS
    b = _block("MoveToCoord")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)
    v, a = __hSpeed, __hAcc
    d = math.sqrt((x - POS[0])**2 + (y - POS[1])**2 + (z - POS[2])**2)
    D = (v**2) / a
    T = 2 * v / a + (d - D) / v if d > D else 2 * math.sqrt(d / a)
    try:
        time = int(time[:-1])/100
        T = int(T * 1000 * time)
    except TypeError:
        T = int(T * 1000 + time)
    Delay(T)
    POS = [x, y, z]
    return T, d

def Circle(n, r, dir = 1):
    """====================\n
    生成圆

    ====================\n
    参数:
        n (int): 平分成n份\n
        r (int): 半径\n
        dir (int, 可选): 方向(1/-1)。默认值为： 1.\n

    Returns:
        list: 圆列表
    """
    return [[round(r * math.cos(i * (dir * 2 * math.pi / n))), round(r * math.sin(i * (dir * 2 * math.pi / n)))] for i in range(1, n)] + [[round(r), 0]]

def Circle_FindPoint(A, B, n, dir = 1):
    """====================\n
    找到圆

    ====================\n
    参数:
        A (list): 圆心坐标[x, y]\n
        B (list): 寻找点坐标[x, y]\n
        n (int/str): 平分成n份\n
        dir (int, 可选): 方向(1/-1)。默认值为： 1.\n
    """
    def distance(A, B):
        return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2)
    try: n = n.split('/')
    except AttributeError: n = [n, n]
    c = [[i[0] + A[0], i[1] + A[1]] for i in Circle(int(n[1]), distance(A, B), dir)]
    return [c[i + 1:] + c[:i + 1] for i in range(int(n[1])) if c[i] == [i for i in c if distance(i ,B) == min(distance(i, B) for i in c)][0]][0][:int(n[0])]

def Move_Circle(x, y, z = 120, n = 8, r = 100, dir = 1, time = 0):
    """====================\n
    移动一个圆

    ====================\n
    参数:
        x (int): 圆心位置x\n
        y (int): 圆心位置y\n
        z (int, 可选): 圆心位置z。默认值为： 120.\n
        n (int, 可选): 平分成n份。默认值为： 8.\n
        r (int, 可选): 半径。默认值为： 100.\n
        dir (int, 可选): 方向(1/-1)。默认值为： 1.\n
        time (int, 可选): 增减延时。默认值为： 0.\n

    Returns:
        int: 总延时
    """
    tot = 0
    for [dx, dy] in Circle(n, r, dir):
        tot += MoveToCoord_AutoDelay(x + dx, y + dy, z, time)[0]
    return tot

def Move_CircleFind(A, B, z = 120, n = 16, dir = 1, time = 0):
    """====================\n
    找到圆并移动

    ====================\n
    参数:
        A (list): 圆心坐标[x, y]\n
        B (list): 寻找点坐标[x, y]\n
        z (int, 可选): 高度。默认值为： 120.\n
        n (int/str, 可选): 平分成n份。默认值为： 16.\n
        dir (int, 可选): 方向(1/-1)。默认值为： 1.\n
        time (int, 可选): 增减延时。默认值为： 0.\n

    Returns:
        int: 总延时
    """
    tot = 0
    for [dx, dy] in Circle_FindPoint(A, B, n, dir):
        tot += MoveToCoord_AutoDelay(dx, dy, z, time)[0]
    return tot

def LedAllOn(color="#ffffff"):
    """====================\n
    飞机灯光变为

    ====================\n
    参数:
        color (str, 可选): 颜色。默认值为： "#ffffff".\n
    """
    b = _block("LedAllOn")
    _field(b, "color", color)

def WaypointRGB(x, y, z, color):
    """====================\n
    直线移至，飞机灯光变为

    ====================\n
    参数:
        x (int): 目标位置x\n
        y (int): 目标位置y\n
        z (int): 目标位置z\n
        color (str): 颜色\n
    """
    MoveToCoord(x, y, z)
    LedAllOn(color)

def LedAllOff():
    """====================\n
    熄灭飞机灯光
    """
    _block("LedAllOff")

def LedBodyOn(color="#ffffff"):
    """====================\n
    机身灯光变为

    ====================\n
    参数:
        color (str, 可选): 颜色。默认值为： "#ffffff".\n
    """
    b = _block("LedBodyOn")
    _field(b, "color", color)

def LedAllBreath(color, delay = 1000, dur = 1000, bright = 1):
    """====================\n
    飞机灯光呼吸

    ====================\n
    参数:
        color (str): 颜色
        delay (int, 可选): 在delay毫秒内逐渐变色。默认值为： 1000.\n
        dur (int, 可选): 在dur毫秒内变暗。默认值为： 1000.\n
        bright (int, 可选): 亮度为bright(0~1)。默认值为： 1.\n
    """
    b = _block("LedAllBreath")
    _field(b, "dur", dur)
    _field(b, "color", color)
    _field(b, "bright", bright)
    _field(b, "delay", delay)

def LedBodyBreath(color, delay = 1000, dur = 1000, bright = 1):
    """====================\n
    飞机机身灯光呼吸

    ====================\n
    参数:
        color (str): 颜色\n
        delay (int, 可选): 在delay毫秒内逐渐变色。默认值为： 1000.\n
        dur (int, 可选): 在dur毫秒内变暗。默认值为： 1000.\n
        bright (int, 可选): 亮度为bright(0~1)。默认值为： 1.\n
    """
    b = _block("LedBodyBreath")
    _field(b, "dur", dur)
    _field(b, "color", color)
    _field(b, "bright", bright)
    _field(b, "delay", delay)

def LedBodyBlink(color, dur, delay, bright):
    """====================\n
    飞机机身灯光持续

    ====================\n
    参数:
        color (str): 颜色\n
        dur (int): 持续dur毫秒\n
        delay (int): delay毫秒后关闭\n
        bright (int): 亮度为bright(0~1)\n
    """
    b = _block("LedBodyBlink")
    _field(b, "color", color)
    _field(b, "birght", bright)
    _field(b, "dur", dur)
    _field(b, "delay", delay)

def LedDroneArmHorse(color1, color2, color3, color4, clock, delay):
    """====================\n
    四个机臂灯光变为

    ====================\n
    参数:
        color1 (str): 颜色1\n
        color2 (str): 颜色2\n
        color3 (str): 颜色3\n
        color4 (str): 颜色4\n
        clock (bool): 顺/逆时针(True/False)\n
        delay (int): 转一圈时间为delay毫秒\n
    """
    b = _block("LedDroneArmHorse")
    _field(b, "color1", color1)
    _field(b, "color2", color2)
    _field(b, "color3", color3)
    _field(b, "color4", color4)
    _field(b, "clock", clock)
    _field(b, "delay", delay)

def LedDroneArmPulse(color1, color2, color3, color4, frequency):
    """====================\n
    四个机臂同亮脉冲

    ====================\n
    参数:
        color1 (str): 颜色1\n
        color2 (str): 颜色2\n
        color3 (str): 颜色3\n
        color4 (str): 颜色4\n
        frequency (int): 频率\n
    """
    b = _block("LedDroneArmPulse")
    _field(b, "color1", color1)
    _field(b, "color2", color2)
    _field(b, "color3", color3)
    _field(b, "color4", color4)
    _field(b, "frequency", frequency)

def finish():
    """====================\n
    结束这架飞机
    """
    global DRONE_NUM, TIME
    TIME = 0
    Vprint("Finished! =========================")
    DRONE_NUM += 1
    if not TEST:
        str_xml = str(ET.tostring(__XML, encoding='utf-8', method="xml"))
        __WEBXML.clear()
        __WEBXML.text = str_xml[2: (len(str_xml) - 1)]

def save():
    """====================\n
    生成代码
    """
    rough_str = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_str)
    new_str = reparsed.toprettyxml(indent='  ')
    f = open('{}.vlfii'.format(FILE), 'w', encoding='utf-8')
    f.write(new_str)
    f.close()
    print("\n\033[33mFile Saved!\033[37m")
    print("""\033[32m

███████╗██████╗  █████╗ ██╗   ██╗███████╗███████╗
██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██╔════╝
█████╗  ██████╔╝███████║ ╚████╔╝ █████╗  ███████╗
██╔══╝  ██╔══██╗██╔══██║  ╚██╔╝  ██╔══╝  ╚════██║
███████╗██║  ██║██║  ██║   ██║   ███████╗███████║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚══════╝╚══════╝

============  Made By EraYes With \033[31m❤\033[32m  ============\033[37m
""")


Move = MoveToCoord
Takeoff = TakeOff
Disarm = Lock
Arm = UnLock
Start = start

音乐 = music
开始 = start
时间 = Time

解锁 = UnLock
上锁 = Lock
延时 = Delay
水平 = Horizontal
垂直 = Vertical
角速度 = AngularVelocity
起飞 = TakeOff
降落 = Land
相对移动 = RelativePosition
移至 = MoveToCoord

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
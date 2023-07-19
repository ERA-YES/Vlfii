import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import math

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

def start(d):
    global FATHER, XML, WEBXML, DRONE
    DRONE = d
    i = DRONE_NUM
    FlightView = ET.SubElement(Flights, "FlightView")
    Ip = ET.SubElement(FlightView, "Ip")
    Ip.text = "192.168.31.10{}".format(i+1)
    InitPos = ET.SubElement(FlightView, "InitPos")
    X = ET.SubElement(InitPos, "X")
    X.text = str(DRONE[i][0])
    Y = ET.SubElement(InitPos, "Y")
    Y.text = str(DRONE[i][1])
    Code = ET.SubElement(FlightView, "Code")
    WEBXML = ET.SubElement(FlightView, "WebXml")
    XML = ET.SubElement(WEBXML, "xml", {"xmlns":"https://developers.google.com/blockly/xml"})
    block = ET.SubElement(XML, "block", {"type":"Goertek_Start", "x":"300", "y":"100"})
    
    FATHER = block

def _next():
    global FATHER
    next = ET.SubElement(FATHER, "next")
    FATHER = next

def _type(t):
    return {"type":"Goertek_"+t}

def _name(n):
    return {"name":n}

def _field(b, n, t):
    field = ET.SubElement(b, "field", _name(n))
    field.text = str(t)

def _block(n):
    global FATHER
    if FATHER.tag != "next" and FATHER.tag != "statement":
        _next()
    b = ET.SubElement(FATHER, "block", _type(n))
    FATHER = b
    return b

def StartTime(time = "00:00", color = "#cccccc"):
    global FATHER, STATEMENT
    b = _block("StartTime")
    _field(b, "time", time)
    _field(b, "color", color)
    statement = ET.SubElement(b, "statement", _name("functionIntit"))
    STATEMENT = b
    FATHER = statement

def End():
    global FATHER
    next = ET.SubElement(STATEMENT, "next")
    FATHER = next

def UnLock():
    '''
    解锁
    '''
    global FATHER
    b = ET.SubElement(FATHER, "block", _type("UnLock"))
    FATHER = b

def Lock():
    _block("Lock")

def Delay(time = 1000):
    b = _block("Delay")
    _field(b, "delay", 0)
    _field(b, "time", time)

def Horizontal(hSpeed = 100, hAcc = 100):
    b = _block("Horizontal")
    _field(b, "hSpeed", hSpeed)
    _field(b, "hAcc", hAcc)

def Vertical(vSpeed = 100, vAcc = 100):
    b = _block("Vertical")
    _field(b, "vSpeed", vSpeed)
    _field(b, "vAcc", vAcc)

def TakeOff(alt=120):
    b = _block("TakeOff")
    _field(b, "alt", alt)

def Land():
    b = _block("Land")

def MoveToCoord(x, y, z = 120):
    global POS
    b = _block("MoveToCoord")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)
    POS = [x, y, z]

def MoveToCoord_AutoDelay(x, y, z = 120, v = 100, a = 100, time = 0):
    global POS
    b = _block("MoveToCoord")
    _field(b, "X", x)
    _field(b, "Y", y)
    _field(b, "Z", z)

    d = math.sqrt((x - POS[0])**2 + (y - POS[1])**2 + (z - POS[2])**2)
    t = v / a
    D = (v**2) / (2 * a)
    if d > 2 * D:
        T = 2 * t + (d - 2 * D) / v
    else:
        T = 2 * math.sqrt(d / a)
    
    T = round(T * 1000)
    d = round(d)

    Delay(T + time)
    POS = [x, y, z]

    return d

def Move_Circle(x, y, z = 120, n = 8, r = 100, d = 1400):
    angle = 2 * math.pi / n
    for i in range(n):
        theta = i * angle
        dx = round(r * math.cos(theta))
        dy = round(r * math.sin(theta))
        MoveToCoord(x + dx, y + dy, z)
        Delay(d)
    MoveToCoord(x + round(r * math.cos(0)), y + round(r * math.sin(0)), z)
    Delay(d)

def Move_Circle_AutoDeplay(x, y, z = 120, n = 8, r = 100, v = 100, a = 100, time = 0):
    angle = 2 * math.pi / n
    for i in range(n):
        theta = i * angle
        dx = round(r * math.cos(theta))
        dy = round(r * math.sin(theta))
        MoveToCoord_AutoDelay(x + dx, y + dy, z, v, a, time)
    MoveToCoord_AutoDelay(x + round(r * math.cos(0)), y + round(r * math.sin(0)), z, v, a, time)

def LedAllOn(color="#ffffff"):
    b = _block("LedAllOn")
    _field(b, "color", color)

def LedBodyOn(color="#ffffff"):
    b = _block("LedBodyOn")
    _field(b, "color", color)

def finish():
    global DRONE_NUM

    str_xml = str(ET.tostring(XML, encoding='utf-8', method="xml"))
    WEBXML.clear()
    WEBXML.text = str_xml[2: (len(str_xml) - 1)]

    DRONE_NUM += 1

def save():
    rough_str = ET.tostring(root, encoding='utf-8', xml_declaration=True)
    reparsed = minidom.parseString(rough_str)
    new_str = reparsed.toprettyxml(indent='  ')
    f = open('output.vlfii', 'w', encoding='utf-8')
    f.write(new_str)
    f.close()


STATEMENT = None
FATHER = None
WEBXML = None
XML = None
POS = [0, 0, 0]
DRONE_NUM = 0

if __name__ == "__main__":
    DRONE = [
        [160, 160],
    ]
    start(DRONE)
    StartTime()
    UnLock()
    Delay()
    Horizontal()
    Vertical()
    TakeOff()
    MoveToCoord(260, 160)
    Delay(2000)
    Land()
    Delay(2500)
    End()
    StartTime()
    LedBodyOn()
    LedAllOn()
    Lock()
    finish()
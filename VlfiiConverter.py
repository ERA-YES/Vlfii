import re

print("请输入：")
lines = []
while True:
    try:
        line = input()
        lines.append(line)
    except:
        break
code = "\n".join(lines)

insert = False 
lines = code.splitlines() 
i = -1 
while True: 
    try: 
        i += 1 
        if lines[i][0:9] == "StartTime": 
            insert = True 
        if lines[i + 1][0:9] == "StartTime" and insert: 
            lines.insert(i + 1, "End()") 
            insert = False 
    except: 
        lines.insert(i + 1, "End()") 
        break 
code = "\n".join(lines)
code = re.sub(r"\n  ", "\n", code)
code = re.sub(r"\n  ", "\n\t", code)
code = re.sub(r"StartTime\((.*?)\)", r'StartTime("\1")', code)
code = re.sub(r"TargetSpeed\((.*?),.*?\)", r'Horizontal(\1,', code)
code = re.sub(r"Acceleration\((.*?),.*?\)", r'\1)', code)
code = re.sub(r",\n", ',', code)
code = re.sub(r"true", '"true"', code)
code = re.sub(r'(#\w+)', r'"\1"', code)
code += "\nfinish()"

print("=======================================================================")
try:
    import pyperclip
    pyperclip.copy(code)
    print(code)
    print()
    print("已复制到剪贴板")
except:
    print(code)
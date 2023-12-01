# a list of all color aliases
colors = {
    "white": "#ffffff",
    "black": "#000000",

    "red": "#ff0000",
    "yellow": "#ffff00",
    "green": "#00ff00",
    "cyan": "#00FFFF",
    "blue": "#0000ff",
    "magenta": "#ff00ff",

    "purple": "#800080",
    "pink": "#FFC0CB",
    "plum": "#C2938D"
}

def h2r(hexCode):
    # replace semicolon with nothing
    hexCode = hexCode.replace(";","")

    # if hexCode is a color alias, convert it
    if hexCode in colors:
        hexCode = colors[hexCode]

    # try convert hex to rgb
    try:
        return tuple(int(hexCode.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
    except Exception as e:
        print(e)
        return (0,0,0)
    
RESET = '\033[0m'

def rgb(c):
    r,g,b = c
    return f"\033[38;2;{r};{g};{b}m"

sys = "[SYSTEM]"
api = "[API]"
view = "[VIEW]"
nav = "[NAVIGATION]"
scene = "[SCENE]"

col_red = "#c03a3e" # "ref"
col_yellow = "#eddd66" # "yellow"
col_blue = "#5865f2" # "blue"
col_green = "#23a55a" # "green"

def log(div,msg,col=""):
    if col == "": col = col_blue
    print(rgb(h2r(col))+div,msg,RESET)
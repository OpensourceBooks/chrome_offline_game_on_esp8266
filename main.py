from machine import Pin,I2C,SPI
import ssd1306
import gfx
from time import sleep

pin_blue = Pin(4, Pin.IN)
pin_red = Pin(5, Pin.IN)

i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)
oled = ssd1306.SSD1306_I2C(128,64, i2c)

#oled = ssd1306.SSD1306_I2C(128, 32, i2c, addr=0x27)
graphics = gfx.GFX(128, 64, oled.pixel)
oled.poweron()
oled.init_display()
oled.fill(0)

oled.show()

def blue_click():
    if(status["is_jumpfinish"]):
        status["is_jump"]=True
        status["is_jumpfinish"]=False

    
def red_click():
    #start game
    if(status["game"]=="ready"):
        status["game"]="playing"
    #fire
    if(status["game"]=="playing"):
        fire()
    #restart game
    if(status["game"]=="gameover"):
        begin()
        status["game"]="playing"
    
def fire():
    pass

status={}

status["game"]="loading"

status["gametime"]=0
status["km"]=0

status["is_jump"]=False
status["is_fire"]=False
status["is_jumpfinish"]=True






player = {}
player["x"] = 10
player["y"] = 44
player["pixel"] = [
        (0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0),
        (0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1,1,1,1),
        (0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1),
        (0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1),
        (0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1),
        (0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0),
        (0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0),
        (0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0),
        (1,0,0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,0,0,0),
        (1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0),
        (1,1,0,0,0,0,1,1,1,1,1,1,1,1,0,1,0,0,0,0),
        (1,1,1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0),
        (1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0),
        (0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0),
        (0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0),
        (0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0),
        (0,0,0,0,1,1,1,1,0,1,1,0,0,0,0,0,0,0,0,0),
        (0,0,0,0,0,1,1,0,0,0,1,0,0,0,0,0,0,0,0,0),
        (0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0),
        (0,0,0,0,0,1,1,0,0,0,1,1,0,0,0,0,0,0,0,0)
    ]

obj={}
obj["x"] = 130
obj["y"] = 44
obj["pixel"] = [
    (0,0,0,0,1,1,1,1,0,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (1,1,0,1,1,1,1,1,1,0,1,1),
    (1,1,0,1,1,1,1,1,1,0,1,1),
    (1,1,0,1,1,1,1,1,1,0,1,1),
    (1,1,0,1,1,1,1,1,1,0,1,1),
    (1,1,0,1,1,1,1,1,1,0,1,1),
    (1,1,0,1,1,1,1,1,1,0,1,1),
    (0,1,1,1,1,1,1,1,1,1,1,0),
    (0,0,1,1,1,1,1,1,1,1,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0),
    (0,0,0,1,1,1,1,1,1,0,0,0)
]


def begin():
    status["game"]="loading"
    status["gametime"]=0
    status["km"]=0
    status["is_jump"]=False
    status["is_fire"]=False
    status["is_jumpfinish"]=True

    obj["x"] = 130
    obj["y"] = 44
    player["y"] = 44


def draw_player():
    
    pixels = player["pixel"]

    if(status["is_jump"]):
        player["y"]-=3
        if(player["y"]<15):
            status["is_jump"]=False
    else:
        player["y"]+=3
        if(player["y"]>=43):
            player["y"]=43
            status["is_jumpfinish"]=True

    for i in range(0,len(pixels)):
        for ii in range(0,len(pixels[i])):
            oled.pixel(player["x"]+ii,player["y"]+i,pixels[i][ii])

def draw_obj():
    obj["x"]-=4

    pixels = obj["pixel"]
    for i in range(0,len(pixels)):
        for ii in range(0,len(pixels[i])):
            oled.pixel(obj["x"]+ii,obj["y"]+i,pixels[i][ii])
    
    if(obj["x"]<=-10):
        obj["x"]=130

def check():
    if(obj["x"]-player["x"]<15 and obj["y"]-player["y"]<15):
        status["game"]="gameover"
    pass
    # pixels_a = player["pixel"]
    # pixels_b = obj["pixel"]


while (True):
    oled.fill(0)
    oled.contrast(1)

    blue = pin_blue.value()
    red = pin_red.value()

    if(pin_red.value() == 0):
        red_click()
    if(status["game"]=="loading"):
        oled.text("loading game.".format(status["km"]),10,30)
        oled.show()
        sleep(1)
        oled.text("loading game..".format(status["km"]),10,30)
        oled.show()
        sleep(1)
        oled.text("loading game...".format(status["km"]),10,30)
        oled.show()
        sleep(1)
        status["game"]="ready"
    if(status["game"]=="ready"):
        oled.text("> play".format(status["km"]),10,20)
        oled.text("code by".format(status["km"]),10,30)
        oled.text("cr4fun".format(status["km"]),10,40)
    if(status["game"]=="playing"):
        if(pin_blue.value() == 0):
            blue_click()
        status["km"]+=1
        status["gametime"]+=1
        graphics.line(0, 63, 127, 63, 1)
        oled.text("{0} km".format(status["km"]),2,0)
        draw_player()
        draw_obj()
        check()
    if(status["game"]=="gameover"):
        oled.text("{0} km".format(status["km"]),2,0)
        oled.text("game over",25,30)
    oled.show()
    
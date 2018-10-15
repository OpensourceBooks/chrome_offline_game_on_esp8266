from machine import Pin,I2C,SPI
import ssd1306
import gfx
from time import sleep
import framebuf
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
    if(status["game"]=="ready"):
        status["game"]="playing"
    elif(status["game"]=="playing"):
        status["game"]="pause"
    elif(status["game"]=="pause"):
        status["game"]="playing"
    elif(status["game"]=="gameover"):
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
player["leg_status"]="1" 


with open('player.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
player["buf_jump"] = framebuf.FrameBuffer(data, 20, 20, framebuf.MONO_HLSB)

with open('player1.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
player["buf1"] = framebuf.FrameBuffer(data, 20, 20, framebuf.MONO_HLSB)

with open('player2.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
player["buf2"] = framebuf.FrameBuffer(data, 20, 20, framebuf.MONO_HLSB)
player["buf"] = player["buf_jump"]

obj={}
obj["x"] = 130
obj["y"] = 44
with open('cacti.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
obj["buf"] = framebuf.FrameBuffer(data, 10, 20, framebuf.MONO_HLSB)

bg={}
bg["x"] = 0
bg["y"] = 53
with open('bg.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
bg["buf"] = framebuf.FrameBuffer(data, 256, 10, framebuf.MONO_HLSB)

with open('gameover.pbm', 'rb') as f:
    f.readline() # Magic number
    f.readline() # Creator comment
    f.readline() # Dimensions
    data = bytearray(f.read())
gameover_buf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)


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
    if(status["is_jump"]):
        player["y"]-=3
        oled.blit(player["buf_jump"], player["x"], player["y"])
        if(player["y"]<15):
            status["is_jump"]=False
    else:
        player["buf"] = player["buf1"]
        player["y"]+=3
        
        if(player["y"]>=43):
            player["y"]=43
            status["is_jumpfinish"]=True
        if (player["leg_status"]=="1" ):
            oled.blit(player["buf1"], player["x"], player["y"])
            player["leg_status"]="2" 
        elif (player["leg_status"]=="2" ):
            oled.blit(player["buf2"], player["x"], player["y"])
            player["leg_status"]="1" 

def draw_obj():
    obj["x"]-=4

    oled.blit(obj["buf"], obj["x"], obj["y"])
    
    if(obj["x"]<=-10):
        obj["x"]=130

def draw_bg():
    bg["x"]-=4

    oled.blit(bg["buf"], bg["x"], bg["y"])
    oled.text("{0} km".format(status["km"]),2,0)
    if(bg["x"]<=-10):
        bg["x"]=0

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

    if(pin_red.value() == 1):
        red_click()
    if(status["game"]=="loading"):
        oled.text("loading.".format(status["km"]),10,30)
        oled.show()
        sleep(1)
        oled.text("loading..".format(status["km"]),10,30)
        oled.show()
        sleep(1)
        oled.text("loading...".format(status["km"]),10,30)
        oled.show()
        status["game"]="ready"
    elif(status["game"]=="ready"):
        oled.text("> play".format(status["km"]),10,20)
        oled.text("code by".format(status["km"]),10,30)
        oled.text("cr4fun".format(status["km"]),10,40)
    elif(status["game"]=="pause"):
        oled.text("pause",25,30)
    elif(status["game"]=="playing"):
        if(pin_blue.value() == 1):
            blue_click()
        status["km"]+=1
        status["gametime"]+=1
        #graphics.line(0, 63, 127, 63, 1)
        draw_bg()
        draw_player()
        draw_obj()
        check()
    elif(status["game"]=="gameover"):
        oled.text("{0} km".format(status["km"]),2,0)
        #oled.text("game over",25,30)
        oled.blit(gameover_buf, 0,25)
    oled.show()
    

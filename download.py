import network
import urequests
import ujson
import time
import gc

def don(filename,url):
    w=urequests.get(url)
    f=open(filename,'wb')
    f.write(w.content)
    f.close()
    print(filename,"Done! free:",gc.mem_free())
    del f,w
    gc.collect()


con={}
con["bli"]="b站ID"
con["city"]="suzhou城市的拼音"
con["keys"]="心知天气私钥"
con["wifiname"]="你的WIFI名称"
con["wifipassword"]="wifi密码"
con["set_password"]="设置esp32的密码"

f=open("config.json",'w')
f.write(ujson.dumps(con))
f.close()

wlan = network.WLAN(network.STA_IF)
wlan.active(True) 
wlan.connect(con["wifiname"], con["wifipassword"]) 

time.sleep(3)



if wlan.isconnected():
    a1="https://webdir.micropython.biz/bilibili/13clock/microWebSrv.py"
    a2="https://webdir.micropython.biz/bilibili/13clock/main.py"
    a3="https://webdir.micropython.biz/bilibili/13clock/ssd1351.py"
    a4="https://webdir.micropython.biz/bilibili/13clock/EspressoDolce18x24.c"
    a5="https://webdir.micropython.biz/bilibili/13clock/FixedFont5x8.c"
    a6="https://webdir.micropython.biz/bilibili/13clock/Robotron7x11.c"
    a7="https://webdir.micropython.biz/bilibili/13clock/Robotron13x21.c"
    a8="https://webdir.micropython.biz/bilibili/13clock/xglcd_font.py"
    don("microWebSrv.py",a1)
    # don("main.py",a2)
    don("ssd1351.py",a3)
    don("EspressoDolce18x24.c",a4)
    don("FixedFont5x8.c",a5)
    don("Robotron7x11.c",a6)
    don("Robotron13x21.c",a7)
    don("xglcd_font.py",a8)
    ourl="https://webdir.micropython.biz/bilibili/13clock/"
    for i in range(39):
        fn=str(i)+".raw"
        url=ourl+fn
        don(fn,url)
    don("main.py",a2)
else:
    print("wifi error")

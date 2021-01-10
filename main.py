from machine import SPI,Pin,RTC
from ssd1351 import Display,color565
from xglcd_font import XglcdFont
import time
import network
import urequests 
import ntptime
import _thread
import ujson
from microWebSrv import MicroWebSrv
import gc

t=time.time()

#oled
spi = SPI(2, baudrate=14500000, sck=Pin(26), mosi=Pin(27))
display = Display(spi, dc=Pin(33), cs=Pin(25), rst=Pin(32),width=128,height=128)

#font导入
robotron = XglcdFont('Robotron13x21.c', 13, 21)
robotronm = XglcdFont('Robotron7x11.c', 7, 11)
espressodolc = XglcdFont('EspressoDolce18x24.c', 18, 24)
fixedfont = XglcdFont('FixedFont5x8.c', 5, 8)


def wjson(a,b,c,d,e,f):
    df={}
    df['wifiname']=a
    df['wifipassword']=b
    df['set_password']=c
    df['bli']=d
    df['keys']=e
    df['city']=f
    f=open("config.json",'wb')
    f.write(ujson.dumps(df))
    f.close()
def showTime():
    rtc=RTC()
    date=rtc.datetime()
    m=date[5]
    h=date[4]
    return [h,m]
def ntp():
    ntptime.host="ntp1.aliyun.com"
    ntptime.NTP_DELTA = 3155644800
    try:
        ntptime.settime()
    except Exception as e:
        pass
def fans(id):
    url="http://api.bilibili.com/x/relation/stat?vmid="+str(id)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE' }
    try:
        re=urequests.get(url,headers=headers)
        my=re.json()
        if my['code']==0:
            return my['data']['follower']
        else:
            return 0
    except Exception as e:
        return 0

def weather(key,city):
    url="http://api.seniverse.com/v3/weather/now.json?key=%s&location=%s&language=zh-Hans&unit=c" % (key,city)
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE' }
    ba=[]
    try:
        # print(url)
        re=urequests.get(url,headers=headers)
        my=re.json()
        ba.append(my['results'][0]['now']['code'])
        ba.append(my['results'][0]['now']['temperature'])
    except Exception as e:
        return False
    return ba

def strx(s):
    if s<10:
        return '0'+str(s)
    else:
        return str(s)

def strb(e,f):
    if e==0:
        return str(f)
    return str(e)


#read config.json 
f=open("config.json","r")
se=ujson.loads(f.read())
f.close()

id=se['bli']
city=se['city']
keys=se['keys']
wifiname=se['wifiname']
wifipassword=se['wifipassword']
set_password=se['set_password']

#ap
ap= network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="mc", authmode=network.AUTH_WPA_WPA2_PSK, password=set_password)
#network
wlan = network.WLAN(network.STA_IF) 
wlan.active(True) 
wlan.connect(wifiname, wifipassword) 


#####自动陪网设置

@MicroWebSrv.route('/')
def _index2(httpClient, httpResponse) :
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        	<meta charset="UTF-8" />
            <title>ESP32时钟</title>
        </head>
        <body class="container">
            <h1>ESP32时钟</h1>
            <br />
			<form action="/" method="post" accept-charset="ISO-8859-1">
				设备密码: <input type="text" name="set_password" class="form-control" value="12345678"><br />
				WIFI名称: <input type="text" name="wifi" class="form-control" value="12345678"><br />
                wifi密码: <input type="password" name="password" class="form-control"><br />
				B站ID: <input type="text" name="bli" class="form-control" value="12345678"><br />
				心知天气key: <input type="text" name="key" class="form-control" value="12345678"><br />
				城市: <input type="text" name="city" class="form-control" value="请输入拼音"><br />
				
				<input type="submit" value="提交修改" class="btn btn-info">
			</form>
        </body>
    </html>
	""" 
	httpResponse.WriteResponseOk( headers= None,contentType	 = "text/html",contentCharset = "UTF-8",content = content )


@MicroWebSrv.route('/', 'POST')
def _post(httpClient, httpResponse) :
    formData  = httpClient.ReadRequestPostedFormData()
    wifi = formData["wifi"]
    password  = formData["password"]
    set_password  = formData["set_password"]
    bli  = formData["bli"]
    key  = formData["key"]
    city  = formData["city"]
    wjson(wifi,password,set_password,bli,key,city)
    content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        	<meta charset="UTF-8" />
            <title>ESP32时钟</title>
        </head>
        <body class="container">
            <div class="jumbotron">
            <h1>ESP32时钟</h1>
            <p>已经完成配置，请重新断开电源。</p>
            </div>
        </body>
        </html>
    """
    httpResponse.WriteResponseOk(headers=None,contentType="text/html",contentCharset="UTF-8",content=content)



# OLED显示
def oledShow(a):
    #初始化时间
    ntp()
    bli=str(fans(id))
    ebli=bli
    wea=weather(keys,city)
    if not wea:
        wea=[0,0]
    img=str(wea[0])+".raw"
    temp=str(wea[1])+"C"
    h,m=showTime()
    mtime=strx(h)+":"+strx(m)

    display.draw_text(5, 40, mtime, robotron, color565(180, 180, 180))
    display.draw_text(127-5*(len(city)+2), 40, city, fixedfont, color565(255, 255, 0))
    display.draw_text(127-13*(len(temp)), 50, temp, espressodolc, color565(255, 255, 0))
    display.draw_text(0, 80, 'bilibili', espressodolc, color565(0, 0,255))
    display.draw_text(0, 110, bli, robotronm, color565(0, 255,255))
    display.draw_image(img,78,78,50,50)
    #循环显示时间
    oh=h
    om=m
    swapMtime=mtime
    swapBli=bli
    while True:
        h,m=showTime()
        if m!=om:
            om=m
            mtime=strx(h)+":"+strx(m)
            display.draw_text(5, 40, swapMtime, robotron, color565(0, 0, 0))
            swapMtime=mtime
            display.draw_text(5, 40, mtime, robotron, color565(220, 220, 220))
            if m%5==0:
                bli=strb(fans(id),ebli)
                display.draw_text(0, 110, swapBli, robotronm, color565(0, 0,0))
                swapBli=bli
                display.draw_text(0, 110, bli, robotronm, color565(0, 255,255))
        if h!=oh:
            ntp()
            bli=strb(fans(id),ebli)
            wea=weather(keys,city)
            if not wea:
                wea=[0,0]
            img=str(wea[0])+".raw"
            temp=str(wea[1])+"C"
            display.clear()
            oh=h
            mtime=strx(h)+":"+strx(m)
            swapBli=bli
            swapMtime=mtime
            display.draw_text(5, 40, mtime, robotron, color565(220, 220, 220))
            display.draw_text(127-5*(len(city)+2), 40, city, fixedfont, color565(255, 255, 0))
            display.draw_text(127-13*(len(temp)), 50, temp, espressodolc, color565(255, 255, 0))
            display.draw_text(0, 80, 'bilibili', espressodolc, color565(0, 0,255))
            display.draw_text(0, 110, bli, robotronm, color565(0, 255,255))
            display.draw_image(img,78,78,50,50)
        time.sleep(1)

if wlan.isconnected():
     _thread.start_new_thread(oledShow,('233',))
else:
    wlan.connect(wifiname, wifipassword) 
    time.sleep(3)
    if wlan.isconnected():
        _thread.start_new_thread(oledShow,('233',))
    else:
        display.draw_text(5, 40, "WIFI Fail", robotron, color565(220, 220, 220))
gc.collect()
srv=MicroWebSrv(webPath=".")
print(time.time()-t)
srv.Start()

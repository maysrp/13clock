# 13clock
ESP32 联合 SSD1351 bilibili时钟
# 准备

1.申请心知天气账号：
https://www.seniverse.com/signup

登入心知天气  

https://www.seniverse.com/products?iid=new
申请免费的天气API
  
在控制台中产品管理》免费版   
其中复制 私钥 即可



# 连线
按以下连接
|esp32|ssd1351|
|-|-|
|VCC|VCC|
|gnd|gnd|
|33|dc|
|32|RES|
|25|CS|
|27|din|
|26|clk|


## 上传
### 常规上传
依次上传里面除download.py以外的所有文件。

### 使用ESP32 自己下载
在进入ESP32后，Ctrl+E
然后将download.py的文件修改后（按照你自己的配置修改相关的内容）  

Ctrl+D
执行 ，

若不行，请重复一次上面的操作，或者查看你的wifi名称和密码是否设置正确


视频教程：  
https://www.bilibili.com/video/BV1uo4y1o7J6

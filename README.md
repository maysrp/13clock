# 13clock
ESP32 联合 SSD1351 bilibili时钟

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
然后将download.py的文件修改后，粘贴上去
Ctrl+D
执行 ，

若不行，请重复一次上面的操作，或者查看你的wifi名称和密码是否设置正确

# ESP32-S3-GEEK + ES5 教程源码

版本：ESPHome 2026.9.1。这是去除个人配置的源码模板，不含可直接烧录的个人固件。

1. 复制 secrets.yaml.example 为 secrets.yaml，填写 2.4GHz Wi-Fi。
2. 用 python -c "import base64,secrets;print(base64.b64encode(secrets.token_bytes(32)).decode())" 生成 api_key，热点密码至少 8 位。
3. 下载思源黑体 SourceHanSansSC-Regular.otf，保存到 fonts/ui.otf；见 fonts/README.md。
4. bash manage.sh compile；bash manage.sh upload --device /dev/ttyACM0（Windows 使用 COM 端口并直接调用 esphome）。
5. HA 添加 ESPHome → Xiaomi BLE，使用自己的 bindkey。
6. 把 geek.yaml 的两项实体占位名称改为 HA 实际生成的 ID，重新编译上传。
7. screen.yaml 修改界面；短按切页、双击旋转、长按息屏。方向保存最多等待 5 秒。

默认 DHCP；不要复制别人的固定 IP。api_key 是 ESPHome 通信密钥，bindkey 是 ES5 广播解密密钥，二者不同。不要发布 secrets.yaml、原始 Flash 或包含个人凭据的编译固件。

## 图文部署教程

https://qianmo.icu/index.php/2026/10/12/esp32-s3-geek-es5-home-assistant-bluetooth-gateway/

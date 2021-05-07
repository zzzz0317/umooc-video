# UMOOC(THEOL) 视频播放器

## 使用许可协议

本程序采用 **GPLv2** 许可协议开源，**严格禁止商业用途和转售牟利**

本软件及所附带的文件是作为 **不提供任何明确的或隐含的赔偿或担保的形式** 提供的。用户出于 **自愿** 而使用本软件，您必须了解使用本软件的 **风险** ，在尚未购买产品技术服务之前，我们不承诺提供任何形式的技术支持、使用担保 ，也 **不承担** 任何因使用本软件而产生问题的相关责任。


## 开始使用前

* Python3 环境
* 请安装 原版 [Chrome浏览器](https://www.google.com/intl/zh-CN/chrome/) 和 [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/home)
* 安装 [Selenium with Python](https://selenium-python.readthedocs.io/)

## 运行

```python3 main.py```

## 更新日志

### v0.4
* 新增文件夹节点遍历功能，默认每个资源打开等待10秒，在```configure.py```中```openAndWaitLink_wait_time```定义，设置为```0```关闭此功能

### v0.3
* 修复可能出现的课程列表获取失败问题
* 添加了版本号显示和更新日志

### 老版本
* v0.2 我忘了
* v0.1 我忘了
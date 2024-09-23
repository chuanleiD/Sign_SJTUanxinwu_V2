# 交大爱心屋每日自动签到

- 用于获取交大爱心屋每日签到奖励：
- 采用selenium库实现具体操作
- 采用《jAccount 验证码在线 ResNet 高速高精度毫秒级识别》by danyang685，中的API实现验证码识别

配置方法：

1. 添加用户名密码：

   修改user.txt中的内容为自己的jAccount用户名及密码，例如：

   ```txt
   testUser1
   testPassword
   ```

2. 安装对应的谷歌浏览器驱动

   参考：https://blog.csdn.net/Z_Lisa/article/details/133307151

   并修改代码中的 Chrome驱动、Chrome浏览器 路径信息：

   ```python
   # 设置Chrome驱动,启动Chrome浏览器
   chrome_url = r"chrome浏览器驱动\chromedriver.exe"
   binary_location = r"chrome浏览器驱动\chrome-win64\chrome.exe"
   ```

3. 配置python环境：

   ```cmd
   pip install -r requirements.txt
   ```

   

#call myvenv\scripts\activate
import base64
import json
import time
import datetime
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions


# 检查今天是否已签到
def check_time():
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	with open("record.txt", "r") as file:
		record_data = file.read()
	if record_data == today:
		return 1
	else:
		return 0


# 标记今天已签到
def mark_today():
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	with open("record.txt", "w") as file:
		file.write(today)


'''def save_captcha_from_selenium(img_elem, save_path):
	# 获取图片的src属性
	# https://jaccount.sjtu.edu.cn/jaccount/captcha?uuid…d5414-5e5b-4ec4-807d-a4528e381547&t=1727061661567
	img_url = img_elem.get_attribute('src')
	print("img_url:" + img_url)

	# 下载图片
	response = requests.get(img_url)

	# 确保响应成功
	response.raise_for_status()

	# 确保目标文件夹存在
	os.makedirs(os.path.dirname(save_path), exist_ok=True)

	# 保存图片
	with open(save_path, 'wb') as file:
		file.write(response.content)

	print(f"Captcha image saved to {save_path}")'''


# 设置Chrome驱动,启动Chrome浏览器
def set_driver(chrome_url, binary_location):
	# 设置Chrome驱动
	chrome_service = Service(chrome_url)

	# 设置Chrome浏览器
	options = Options()
	options.binary_location = binary_location
	options.add_argument('-ignore-certificate-errors')
	options.add_argument('-ignore-ssl-errors')
	# options.add_argument('--headless')  # 示例: 无界面模式

	# 启动Chrome浏览器
	driver = webdriver.Chrome(service=chrome_service, options=options)
	return driver


def jump_to_jAccount(driver, jAccount_url):
	# 打开jAccount登录页面
	driver.get(jAccount_url)
	time.sleep(2)

	# 点击登录按钮
	login_button = driver.find_element(By.XPATH, "//button[@class='ant-btn css-1y13rdz ant-btn-primary']")
	login_button.click()
	time.sleep(2)


# 从Selenium中获取验证码图片的base64编码
def get_captcha_image(driver):
	# 获取图片的base64编码
	img_base64 = driver.execute_script("""
		var canvas = document.createElement('canvas');
		var context = canvas.getContext('2d');
		var img = document.querySelector('#captcha-img');
		canvas.height = img.naturalHeight;
		canvas.width = img.naturalWidth;
		context.drawImage(img, 0, 0);
		return canvas.toDataURL('image/jpeg').substring(22);
	""")
	return base64.b64decode(img_base64)


# 识别验证码，返回字符串结果
def recognize_captcha(img_data):
	url = "https://plus.sjtu.edu.cn/captcha-solver/"
	files = {'image': ('captcha.jpg', img_data, 'image/jpeg')}
	response = requests.post(url, files=files)
	return json.loads(response.text)["result"]


# 一次：登录并检查是否成功
def login_and_check(driver, username, password):
	# 获取验证码结果
	# jAccount 验证码在线 ResNet 高速高精度毫秒级识别
	# by danyang685
	img_data = get_captcha_image(driver)
	captcha_text = recognize_captcha(img_data)

	# 找到输入框，这里需要自行在F12的Elements中找输入框的位置，然后在这里写入
	user_input = driver.find_element(By.XPATH, '//*[@id="input-login-user"]')
	pw_input = driver.find_element(By.XPATH, '//*[@id="input-login-pass"]')
	verification_code = driver.find_element(By.XPATH, '//*[@id="input-login-captcha"]')

	# 输入用户名和密码，点击登录
	user_input.send_keys(username)
	pw_input.send_keys(password)
	verification_code.send_keys(captcha_text)
	time.sleep(0.2)

	# 提交
	start = driver.find_element(By.XPATH, '//*[@id="submit-password-button"]')
	start.click()
	time.sleep(0.5)


if __name__ == '__main__':

	if check_time() == 100:
		print("今日已签到")
		os.system("taskkill /f /im cmd.exe")  # 关闭cmd窗口
	else:
		with open("user.txt", "r") as f:
			data = f.read().splitlines()
		username = data[0]
		password = data[1]

		# 设置Chrome驱动,启动Chrome浏览器
		chrome_url = r"chrome浏览器驱动\chromedriver.exe"
		binary_location = r"chrome浏览器驱动\chrome-win64\chrome.exe"
		driver = set_driver(chrome_url, binary_location)

		# 打开jAccount登录页面
		jAccount_url = r"https://aixinwu.sjtu.edu.cn/"
		jump_to_jAccount(driver, jAccount_url)

		login_flag = False
		for i in range(0, 2):  # 重试两次
			login_and_check(driver, username, password)
			current_url = driver.current_url
			if current_url.startswith("https://aixinwu.sjtu.edu.cn/"):
				print(f"当前页面的 URL 是: {current_url}")
				login_flag = True
				break
			else:
				print(f"当前页面的 URL 是: https://jaccount.sjtu.edu.cn/jaccount/...")
				print("登录失败，重试中...")
				driver.refresh()
				time.sleep(1)
		driver.close()

		if login_flag:
			mark_today()
			print("success!")
		else:
			print("登录失败，请检查用户名、密码和验证码识别是否正确！")
			time.sleep(3)
	# os.system("taskkill /f /im cmd.exe")  # 关闭cmd窗口

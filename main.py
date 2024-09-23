#call myvenv\scripts\activate 

from selenium import webdriver
import time
import datetime
import os
import requests

def check_time():
	today = datetime.datetime.now().strftime('%Y-%m-%d')
	with open("record.txt", "r") as file:
		record_data = file.read()

	if record_data == today:
		return 1
	else:
		with open("record.txt", "w") as file:
			file.write(today)
		return 0


def save_captcha_from_selenium(web_driver, save_path):
	# 找到图片元素
	img_elem_web = web_driver.find_element_by_id("captcha-img")

	# 获取图片的src属性
	# https://jaccount.sjtu.edu.cn/jaccount/captcha?uuid…d5414-5e5b-4ec4-807d-a4528e381547&t=1727061661567
	img_url = img_elem_web.get_attribute('src')
	img_url = r"https://jaccount.sjtu.edu.cn/jaccount/" + img_url
	print("img_url:"+img_url)

	# 下载图片
	response = requests.get(img_url)

	# 确保响应成功
	response.raise_for_status()

	# 确保目标文件夹存在
	os.makedirs(os.path.dirname(save_path), exist_ok=True)

	# 保存图片
	with open(save_path, 'wb') as file:
		file.write(response.content)

	print(f"Captcha image saved to {save_path}")



if __name__ == '__main__':

	if check_time() == 1:
		print("今日已签到")
		os.system("taskkill /f /im cmd.exe")  # 关闭cmd窗口
	else:
		with open("user.txt", "r") as f:
			data = f.read().splitlines()
		username = data[0]
		password = data[1]

		jAccount_url = r"https://aixinwu.sjtu.edu.cn/"
		chrome_url = r"chrome浏览器驱动\chromedriver.exe"

		# 打开网页链接
		options = webdriver.ChromeOptions()
		options.binary_location = r"chrome浏览器驱动\chrome-win64\chrome.exe"
		options.add_argument('-ignore-certificate-errors')
		options.add_argument('-ignore-ssl-errors')
		driver = webdriver.Chrome(executable_path=chrome_url, chrome_options=options)

		driver.get(jAccount_url)
		time.sleep(2)
		login_button = driver.find_element_by_xpath("//button[@class='ant-btn css-1y13rdz ant-btn-primary']")
		login_button.click()
		time.sleep(2)

		img_elem = driver.find_element_by_id("captcha-img")
		print("find_captcha-img")

		# 保存Canvas上的图片到本地
		picture_url = r"picture\captcha.jpg"
		img_elem.screenshot(picture_url)

		ocr = ddddocr.DdddOcr()
		with open(picture_url, 'rb') as f:
			img_bytes = f.read()
		# 本地OCR
		res = ocr.classification(img_bytes)
		print(res)

		# 找到输入框，这里需要自行在F12的Elements中找输入框的位置，然后在这里写入
		user_input = driver.find_element_by_xpath('//*[@id="input-login-user"]')
		pw_input = driver.find_element_by_xpath('//*[@id="input-login-pass"]')
		verification_code = driver.find_element_by_xpath('//*[@id="input-login-captcha"]')

		# 输入用户名和密码，点击登录
		user_input.send_keys(username)
		pw_input.send_keys(password)
		verification_code.send_keys(res)

		time.sleep(0.2)

		# 提交
		start = driver.find_element_by_xpath('//*[@id="submit-password-button"]')
		start.click()
		time.sleep(0.3)

		# 刷新页面
		driver.refresh()

		driver.close()
		print("success!")

		os.system("taskkill /f /im cmd.exe")  # 关闭cmd窗口

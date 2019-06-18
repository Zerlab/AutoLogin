import time
import requests
import re
import base64
from selenium import webdriver
from selenium.webdriver import ActionChains


class com12306(object):
    def __init__(self):
        self.url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"}

    def run(self):
        # 创建chrome对象, 发送get请求
        chrome = webdriver.Chrome()
        chrome.get(self.url)
        time.sleep(2)
        # 点击账号登录
        chrome.find_element_by_xpath ('/html/body/div[2]/div[2]/ul/li[2]').click()

        # 获取输入框元素, 输入账号密码
        time.sleep(2)
        chrome.find_element_by_id('J-userName').send_keys('your username')
        chrome.find_element_by_id('J-password').send_keys('your passwrod')

        time.sleep(3)
        #下载验证码图片
        pic_url = chrome.find_element_by_class_name('imgCode').get_attribute('src')
        pic_url = str(pic_url).replace('data:image/jpg;base64,', '')
        check_res = base64.b64decode(pic_url)

        # 将验证码保存到本地
        with  open('checkPic.jpg', 'wb')  as  f:
            f.write(check_res)
            print('图片下载成功！')

        #解析验证码
        toolUrl='http://littlebigluo.qicp.net:47720/'
        files={'pic_xxfile':('checkPic.jpg',open('checkPic.jpg','rb'),'image/jpg',{})}
        resPic=requests.request("POST",toolUrl,data={"type":"1"},files=files)

        #获取验证码序列
        picNumTry=resPic.text.split('<B>')[1]
        picNum=picNumTry.split('</B>')[0]
        print(picNum)
        picNumT=picNum.split(' ')
        print(picNumT)

        #点击验证码图片
        for i in range(len(picNumT)):
            time.sleep(1)
            j=int(picNumT[i])
            imgelement = chrome.find_element_by_xpath('//*[@id="J-loginImg"]')
            if j <= 4:
                ActionChains(chrome).move_to_element_with_offset(imgelement, 40 + 72 * (j - 1),73).click().perform()
            else:
                j -= 4
                ActionChains(chrome).move_to_element_with_offset(imgelement, 40 + 72 * (j - 1),145).click().perform()

        #点击登录
        chrome.find_element_by_xpath('//*[@id="J-login"]').click()

        time.sleep(10)
        chrome.quit()


def main():
    db = com12306()
    db.run()


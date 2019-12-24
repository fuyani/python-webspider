from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import *
import time
from threading import Timer

class Jsyx():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.get("http://study.huatec.com/")
        self.wait = WebDriverWait(self.browser,10)

    def login(self):
        time.sleep(4)
        button = self.browser.find_element_by_xpath("//*[@id='bannerLogin']")
        button.click()
        user = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='login-pop']/div/form/div[1]/div[1]/input")))
        user.send_keys(uname)
        password = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='login-pop']/div/form/div[1]/div[3]/input")))
        password.send_keys(paswd)
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='login-pop']/div/form/button")))
        login_button.click()
        name = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='islogin']/h4")))
        time.sleep(1)
        print("%s 登录成功！"%name.text)

    def start_handing(self):
        button = self.wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='toSpace']")))
        button.click()
        for i in range(courses):
            course = self.wait.until(EC.presence_of_element_located((By.XPATH,"//li[@class='course-item'][{}]/div[1]".format(i))))
            course.click()
            self.browser.switch_to.window(self.browser.window_handles[i+1])
            time.sleep(2)
            course1_handing = self.wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='course-list-right']/h4")))
            course1_handing.click()
            time.sleep(2)
            try:
                video = self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='my-video']")))
                video.click()
            except:
                pass
            print("开始挂第{}门课程".format(i+1))
            self.browser.switch_to.window(self.browser.window_handles[0])

    def close(self):
        self.browser.close()
        print('挂学时结束！')

    def main(self):
        self.login()
        self.start_handing()
        t = Timer(stop_time*60,self.close)
        t.start()

if __name__ == '__main__':
    run = Jsyx()
    run.main()
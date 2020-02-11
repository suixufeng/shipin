from selenium import webdriver
from selenium.webdriver.common.by import By  #引用网页选择器
from selenium.webdriver.support.ui import WebDriverWait  #引用设定显示等待时间
from selenium.webdriver.support import expected_conditions as EC  #引用等待条件
import time
import threading
 
#————————————天眼查大类————————————————
class Tianyan():
 
    def __init__(self,user,pwd):
        self.browser=webdriver.Chrome()  #实例化浏览器对象，并命名为 browser
        self.user=user
        self.pwd=pwd
        self.wait=WebDriverWait(self.browser,15) #设定浏览器最大等待时间为5秒钟，超过就报错
        self.get_url()
 
 
#————————————触发浏览器对象————————————
    def get_url(self):

        self.browser.get("https://www.qichacha.com/") #打开天眼查浏览器
        #button=self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME,"link-white"))) #等待目标可以点击
        button=self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="web-content"]/div/div[1]/div[1]/div[1]/div/div[2]/div/div[4]/a')))
        button.click()
        #button2=self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="login-warp"]/div[1]/div[3]/div[1]/div[2]')))
        #button2.click()
        
        time.sleep(2)
        button2=self.wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="dialog_61550553"]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[2]')))
        button2.click()
 
 
#———————————公司文本————————————
    def write(self):
        with open(doc_company,"rb") as f:
            for i in f :
                yield i.decode(encoding='utf-8')
 

#———————————登录——————————————————
    def check_login(self):
        try:
            input_user = self.browser.find_element_by_xpath('//*[@id="mobile"]')
            input_psw = self.browser.find_element_by_xpath('//*[@id="password"]')
            #input_user = self.browser.find_element_by_xpath('//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[2]/input')
            #input_psw = self.browser.find_element_by_xpath('//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[3]/input')
            input_user.send_keys(self.user) #发送登录账号
            input_psw.send_keys(self.pwd)
            time.sleep(1)  #等待 一秒 防止被识别为机器人
            login=self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="login-warp"]/div[1]/div[3]/div[2]/div[5]')))
            login.click()
            return True
        except Exception as ex:
                print("出现如下异常%s"%ex)
 
# ———————————发送要查询公司的名称——————————————————
    def check_company(self,company):
        company_input = self.browser.find_element_by_id("home-main-search")
        company_click = self.wait.until(EC.element_to_be_clickable((By.XPATH,'//div[@class="input-group-btn btn -hg"]')))
        company_input.send_keys(company)
        time.sleep(0.2)
        company_click.click()
 
# ————————————获取要查询的公司的名称、法人、电话信息—————————————————
    def get_news(self):
        name = self.browser.find_element_by_xpath('//div[@class="header"]/a/em').text
        faren = self.browser.find_element_by_xpath('//div[@class="info"]/div[1]/a').text
        phone = self.browser.find_element_by_xpath('//div[@class="contact"]/div[1]/span[2]').text
        company_list = "公司名称：|%s |法人：| %s|电话：| %s" % (name, faren, phone)
 
        self.downlode_company(company_list) #存储信息
        print(company_list)
 
#———————————存储需要时保存的信息——————————————————
    def downlode_company(self,data):
        with open(doc_check_company, "a", encoding="utf-8") as f:
            f.write(data)
            f.write("\n")
 
# ———————————主要运行逻辑——————————————————
    def main(self):
        if self.check_login(): #
            f=self.write()
            for company in f:
                try:
                    self.check_company(company)
                    get_thread=threading.Thread(target=self.get_news()) #使用线程来存储信息
                    get_thread.start()
                    self.browser.back()
                except:
                    message = '公司名称：|%s|该公司电话法人资料不齐全，无法抓取' % company
                    print(message)
                    self.downlode_company(message)
                    self.browser.back()
             
        else:
            print("账号密码不正确，请重新核对")
 
 
#———————————主体参数———————————————————————
if __name__ == '__main__':
    user='15166######56'                 #账号
    pwd='518518####18'                #密码
    doc_check_company='check_company.txt'  #查询之后的公司名称
    doc_company='company.txt'   #需要查询的公司列表
    time1=time.time()  
    window=Tianyan(user,pwd)
    window.main()
    time2=time.time()
    print(time2-time1)
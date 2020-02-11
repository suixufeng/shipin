import requests
from bs4 import BeautifulSoup
import csv
import time
import random
import csv
import re
#信息写入csv文件
def write_data(data,name):
    file_name=name
    with open(file_name, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["手机号码", "电话号码","联 系 人","公司名称"])
        #writer.writerows([data])
        for each in data:
            writer.writerow(each)
        print('抓取完成') 


#批量爬取https://www.21food.cn/ 相关公司联系方式等
def get_content(url,data=None):
    
    user_agents = ['Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50','Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11']
    cookies = dict(uuid='b18f0e70-8705-470d-bc4b-09a8da617e15',UM_distinctid='15d188be71d50-013c49b12ec14a-3f73035d-100200-15d188be71ffd')
    header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'User-Agent':random.choice(user_agents),
    }
    #totals=[]
    for each in pro_id: 
        try:
            #url="https://www.21food.cn/product/detail"+str(each)+".html"
            print(url)
            #time.sleep(random.randint(0,3)) 
           
            # s = requests.session()
            # s.keep_alive = False
            # s.proxies = {"https": "116.196.85.150:9999"}
            # s.headers = {
            # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
            # }
            #r = s.get(url)
            #requests.adapters.DEFAULT_RETRIES = 5
            
            
            #proxy = random.choice(self.urlproxylist)
            #proxies = {"https": "111.35.245.203:9999"}
            #通过代理API获取可用的代理IP
            proxys=requests.get('http://kuyukuyu.com/agents/get?uuid=56e9183d-8f4e-4c5f-9610-4051256fcbd9')
            proxy={"https": proxys.text}
            r = requests.get(url, headers=header,proxies = proxy,cookies = cookies,timeout=5)
            #r = requests.get(url, headers=header,cookies = cookies,timeout=8)
            print(r.raise_for_status)
            try:
                    soup = BeautifulSoup(r.content, 'html.parser')
                    
                    rows=[]
                    for span in soup.find_all('dd', class_=['bm_gh1','bm_gh2','bm_gh3','bm_gh4']):
                        #rows=[]
                        #print(span.get_text())
                        tel = span.text
                        if len(tel):
                            rows.append(tel)
                        
                        #rows.append(span.get_text())
                        #pthons.append(rows) 
                        #print(rows)              
                    for sp1 in soup.find_all('dl',class_=['dft_pgf1']):
                        title=sp1.find_all('a')
                        if len(title):
                            try:
                                rows.append('主营业务：'+title[1].get_text())
                            except Exception as ex:
                                pass
                    #time.sleep(random.randint(1,3))     
                    return rows
                    
            except Exception as ex:
                    print("出现如下异常%s"%ex)
        
        except Exception as ex:
            print("出现如下异常%s"%ex)
            continue
 #write_data(pthons,'phone.csv')

if __name__ == '__main__':
    #pro_id=[1325514,1571224,286464,298857,1496610,1503217,1362390,1195259,1231220,1094695,1061515,1011721,31990]
    
    pro_id = input("复制粘贴网页上pro_id的值：")
    pro_idlist=pro_id.split(",")
    pthons=[]

    for each in pro_idlist: 
        url="https://www.21food.cn/product/detail"+str(each)+".html"
        #url="https://baidu.com"
        #proxies = getListProxies()
        mydata = get_content(url)
        #mydata=['1','2','3']
        if len(mydata):
            pthons.append(mydata) 
        #pthons.append('\r\n') 
        
        if len(pthons):
            write_data(pthons,'phone.csv')
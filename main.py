from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from tqdm import tqdm
import pandas as pd



cars = [ '경차', '소형차','준중형차', '중형차', '대형차', '스포츠카', 'SUV', 'RV']

driver = webdriver.Chrome()

for i in tqdm(cars):
    
    page = 1
    car_info = []
    ispage = True

    while ispage == True:
        url = 'http://www.encar.com/dc/dc_carsearchlist.do?carType=kor&searchType=model&wtClick_kor=003&TG.R=A#!%7B%22action%22%3A%22(And.Hidden.N._.CarType.Y._.Category.{}.)%22%2C%22toggle%22%3A%7B%7D%2C%22layer%22%3A%22%22%2C%22sort%22%3A%22ModifiedDate%22%2C%22page%22%3A{}%2C%22limit%22%3A20%7D'

        driver.get(url.format(i, page))

        time.sleep(5)
        
        tbody = driver.find_element_by_xpath('//*[@id="sr_normal"]')
        
        trs = tbody.find_elements_by_xpath('.//tr')
        
        #더 이상 차량 정보가 없을시 다음 차량 타입으로 넘어감
        if len(trs) == 0:
            ispage = False
            continue
        
        time.sleep(3)

        if len(trs) != 0:
            for tr in tqdm(trs):
                company = tr.find_element_by_xpath('.//td[2]/a/span[1]/strong').text.split('(')[0]
                if len(company) == 0 :
                    continue      
                name = tr.find_element_by_xpath('.//td[2]/a/span[1]/em').text.replace(' ', '').split('(')[0]   
                year = tr.find_element_by_xpath('.//td[2]/span[1]/span[1]').text.split('/')[0]
                km = tr.find_element_by_xpath('.//td[2]/span[1]/span[2]').text.replace(',', '').replace('km', '')
                fuel = tr.find_element_by_xpath('.//td[2]/span[1]/span[3]').text.split('(')[0]
                price = tr.find_element_by_xpath('.//td[3]/strong').text.replace(',', '').replace('"', '')
        
                car_info.append({
                        'company' : company,
                        'name' : name,
                        'year' : int(year),
                        'km' : int(km), 
                        'fuel': fuel,
                        'price' : int(price)
                    })      
        
       
        data = pd.DataFrame(car_info)
        data.to_csv('{}_info.csv'.format(i), index = False)
        print('{} {} {}페이지까지 저장완료'.format(int(len(car_info)), i, page))
        
        page += 1

            
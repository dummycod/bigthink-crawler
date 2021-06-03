from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
import time

class WebCrawler:

	def openAndClose(url,timesToOpen,closingTime):
		driver = webdriver.Chrome()
		for x in range(timesToOpen):
			driver.get(url)
			time.sleep(3)
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(closingTime)
		driver.close()

	def getAllUrlsForGivenSection(url):
		options = Options()
		options.add_extension('uBlock Origin 1.35.2.0.crx')
		driver = webdriver.Chrome(options=options)
		driver.get(url)
		driver.maximize_window()
		time.sleep(3)
		for x in range(50):
			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		text=driver.page_source
		soup = BeautifulSoup(text.encode('utf-8'),'html.parser')
		for tag in soup.find_all('a',{'class':"widget__headline-text"}):
			print(tag['href'].encode('cp1252', errors='ignore'))
		driver.close()

	def playBigthinkAudio(url):
		options = Options()
		options.add_extension('uBlock Origin 1.35.2.0.crx')
		driver = webdriver.Chrome(options=options)
		driver.get(url)
		time.sleep(3)
		iframe = driver.find_element_by_class_name('remixd-frame')
		driver.switch_to.frame(iframe)
		driver.find_element_by_xpath('/html/body/div[2]/div[1]').click()
		time.sleep(10)
		while(True):
			timer=driver.find_element_by_xpath('//*[@id="playerRemainingDuration"]')
			if(timer.text=="00:00"):
				break
		driver.find_element_by_xpath('/html/body/div[2]/div[1]').click()


#WebCrawler.getAllUrlsForGivenSection('https://bigthink.com/surprising-science/')
WebCrawler.playBigthinkAudio('https://bigthink.com/surprising-science/dark-matter-bridges-future-galaxy')
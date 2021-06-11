from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from trie import Trie  
import time
import requests

class WebCrawler:


	def __init__(self,timesToOpen,closingTime,level,audio):
		self.timesToOpen = timesToOpen #how many times site must be open
		self.closingTime = closingTime #after how much seconds site must be closed
		self.trie = Trie()  #trie to store the links
		self.options = Options() 
		self.options.add_extension('uBlock Origin 1.35.2.0.crx') #extention
		self.level = level	 #how deep website has to be crawled (may increase time upto 1 hour if set high)
		self.audio= audio #bool to set if the audio must be played or not


	def openAndClose(self,url):
		for x in range(self.timesToOpen):
			self.driver.get(url)
			time.sleep(3)
			if self.audio:
				self.playAudio()
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(self.closingTime)
		


	def getSections(self,url):
		response=requests.get(url)
		text = response.text
		soup = BeautifulSoup(text,'html.parser')
		links = soup.find('div',{'id':'sTop_Bar_0_0_6_0_0_6_1_0_1_0_1_1'})
		sectionsList = []
		
		for tag in links:
			sectionsList.append(tag['href'][1:])
		
		return sectionsList

		
	def getSectionArticles(self,section):
		
		sectionUrl = 'https://bigthink.com/'+section
		self.driver.get(sectionUrl)
		time.sleep(2)
		
		for x in range(self.level):
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			time.sleep(2)
		
		text=self.driver.page_source
		soup = BeautifulSoup(text.encode('utf-8'),'html.parser')
		tagList = soup.find_all('a',{'class':"widget__headline-text"})

		for tag in tagList:
			link = tag['href']
			self.trie.add(link)



	def playAudio(self):
		try:
			iframe = self.driver.find_element_by_class_name('remixd-frame')
			self.driver.switch_to.frame(iframe)
			self.driver.find_element_by_xpath('/html/body/div[2]/div[1]').click()

		except:
			print('No Audio Found')

		else:
			time.sleep(10)
			while(True):
				timer=self.driver.find_element_by_xpath('//*[@id="playerRemainingDuration"]')
				if(timer.text=="00:00"):
					break
			self.driver.find_element_by_xpath('/html/body/div[2]/div[1]').click()


	def postmortem(self,url):
		sectionsList = self.getSections(url)
		
		self.driver = webdriver.Chrome(options= self.options)

		for section in sectionsList:
			self.getSectionArticles(section)

		self.trie.traverse(self.openAndClose)

		self.driver.close()


webCrawler = WebCrawler(timesToOpen=2,closingTime=2,level=1,audio=True)
webCrawler.postmortem('https://bigthink.com')





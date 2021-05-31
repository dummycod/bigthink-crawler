from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

url = "https://stackoverflow.com/questions/32391303/how-to-scroll-to-the-end-of-the-page-using-selenium-in-python"
WebCrawler.openAndClose(url= url,timesToOpen=5,closingTime=3)
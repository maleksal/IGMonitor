import json
import pickle
import time
from datetime import datetime

from app.helpers import handle_cookies, scroll_down
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Client:
	"""
	Client - scrapes data from instagram website using selenium.
	Attributes:
		base_url:		Link to instagram website
		username:		Instagram username
		password:		Instagram password
		target:			Target to be monitored
		cookie_file:	Optional file name 'where to save/retrieve cookies'

	"""

	def __init__(self, base_url, username, password, target, cookie_file='cookies.pkl'):
		'''Client Class constuctor.'''

		self.base_url = base_url
		self.username = username
		self.password = password
		self.target = target
		self.cookie_file = cookie_file
		self.cookies = None
		# settings for not showing the browser 
		options = webdriver.FirefoxOptions()
		options.add_argument("--headless")
		options.add_argument("--disable-gpu")
		options.add_argument("--no-sandbox")
		options.add_argument("enable-automation")
		options.add_argument("--disable-infobars")
		options.add_argument("--disable-dev-shm-usage")
		self.driver = webdriver.Firefox(options=options)

	def authenticate(self):
		"""
		Handles authentication with instagram, either by cookies or password.
		"""
		if cookies_data := handle_cookies(self.cookie_file):
			self.cookies = cookies_data
			self.driver.get(self.base_url)
			# push cookies to browser
			for cookie in self.cookies:
				self.driver.add_cookie(cookie)
		else:
			self.driver.get('https://www.instagram.com/accounts/login/?next=login&source=desktop_nav')
			self.driver.implicitly_wait(5)
			self.driver.find_element_by_name('username').send_keys(self.username)
			self.driver.find_element_by_name('password').send_keys(self.password + Keys.ENTER)
			time.sleep(6)
			# load cookies from browser
			pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))
			return self.authenticate()

	def navigate_target_profile(self):
		self.driver.get(self.base_url + self.target)

	def load_followers_or_followings(self, _type=None):
		'''
		Using selenium to click followers or followings and scrols al way down,
		takes a string argument wich is either followers or follwing.
		Returns:
			int: Total followers or followings
		'''
		self.navigate_target_profile()
		xpath = {
			'followers': '/html/body/div[1]/section/main/div/header/section/ul/li[2]/a',
			'followings': '/html/body/div[1]/section/main/div/header/section/ul/li[3]/a'
			}
		# click to reveal popup
		self.driver.implicitly_wait(3)
		self.driver.find_element_by_xpath(xpath[_type]).click()
		self.driver.implicitly_wait(5)
		# scroll down
		fBody  = self.driver.find_element_by_xpath("//div[@class='isgrP']")
		return scroll_down(fBody, self.driver)

	def get_followings(self):
		'''
		Gets target followings from instagram website using selenium.
		Returns:
			total_followings:	number of total followings.
			followings:			list of usernames following target.
		'''

		followings = []
		total_followings = self.load_followers_or_followings('followings')
		# Extract usernames
		for i in range(1, total_followings + 1):
			user = self.driver.find_element_by_xpath(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[1]/div[2]/div[1]/span')
			followings.append(user.text)
		return (total_followings, followings)

	def get_followers(self):
		'''
		Gets target followers from instagram website using selenium.
		Returns:
			total_followers:	<int> number of total followers.
			followers:			<list> usernames of those followers.
		'''

		followers = []
		total_followers = self.load_followers_or_followings('followers')
		# Extract usernames
		for i in range(1, total_followers + 1):
			user = self.driver.find_element_by_xpath(f'/html/body/div[5]/div/div/div[2]/ul/div/li[{i}]/div/div[1]/div[2]/div[1]/span')
			followers.append(user.text)
		return (total_followers, followers)

	def close(self):
		self.driver.quit()

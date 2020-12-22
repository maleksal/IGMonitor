"""
Some helper functions
"""

import os
import pickle
import time
from datetime import timedelta


def handle_cookies(filename):
	"""
	Loads cookie form file and checks for expiry date.
	Returns: loaded cookie or None
	"""
	cookies = None
	# check & validate cookies
	if os.path.exists(filename):
		cookies = pickle.load(open(filename, "rb"))
		for cookie in cookies:
			if 'expiry' in cookie.values():
				expires = datetime.now() + timedelta(seconds=cookie['expiry'])
				if expires < datetime.now(): 
					os.remove(filename)
					return handle_cookies(filename)
	return cookies


def find_missing(src, dest):
	"""
	Find missing items from src in dest.
	Returns: list of missing items.
	"""
	missing = [item for item in src if item not in dest]
	return missing


def scroll_down(fBody, driver):
	"""
	Scrolls down a page using selenium.
	Arguments:
		fBody: 		targeted html element.
		driver: 	selenium driver.

	Returns: number of total elements 
	"""
	overflow = 0
	extracted = 0
	detection = 0
	while True:
		detection = extracted
		driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
		time.sleep(0.3)
		extracted = len(driver.find_elements_by_xpath("//div[@class='isgrP']//li"))
		if extracted == detection:
			overflow += 1
			if overflow >= 10: # break
				break
		else:
			overflow = 0
	return extracted

def add_to_list(src, dest):
	for i in src:
		dest.append(i)

def remove_from_list(src, dest):
	for i in src:
		dest.remove(i)	

def spinner(threadd):
	eli_count = 0
	while threadd.is_alive():
		print('[ processing ]', '.'*(eli_count+1), ' '*(2-eli_count), end='\r')
		eli_count = (eli_count + 1) % 3
		time.sleep(0.2) 

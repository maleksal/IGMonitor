"""
Application module
"""
import time
from datetime import datetime

from app.client import Client
from app.display import Display
from app.helpers import add_to_list, find_missing, remove_from_list
from app.storage import Storage


class Application:
	'''Main logic.''' 

	def __init__(self, base_url, username, password, target):
		'''Application constructor.'''
		self.db = Storage(target + '.json')
		self.client = Client(base_url, username, password, target)
		self.client.authenticate()
		if self.db.retrieve():
			# If user found assign it to self.user
			# Add atts like follwings && unfollowings
			self.user = self.db.retrieve()
			self.display = Display(self.user)

	def register_user(self):
		'''Creates a new user, to be monitored next time.'''
		total_followings, followings = self.client.get_followings()
		total_followers, followers = self.client.get_followers()
		user = {
			'date': datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
			'username': self.client.target,
			'total-followings': total_followings,
			'total-followers': total_followers,
			'followings': followings,
			'followers': followers
		}
		self.db.save(user)

	def report_followings(self):
		"""Reports target new followings && unfollowings."""
		followings, unfollowings = [], []
		current_followings = self.user['followings']			# old user followings
		total, new_followings = self.client.get_followings()	# new user followings
		if self.user['total-followings'] != total:
			if total > self.user['total-followings']:
				self.user['total-followings'] = total
				follwings = find_missing(new_followings, current_followings)
				add_to_list(followings, self.user['followings'])
			else:
				self.user['total-followings'] = total
				unfollowings = find_missing(current_followings, new_followings)
				remove_from_list(unfollowings, self.user['followings'])
			self.db.save(user)
		self.display.followings_report(followings, unfollowings)

	def report_followers(self):
		"""Reports target new followers && unfollowers."""
		followers, unfollowers = [], []
		current_followers = self.user['followers']				# old user followers
		total, new_followers = self.client.get_followers()		# new user followers
		if self.user['total-followers'] != total:
			if total > self.user['total-followers']:
				self.user['total-followers'] = total
				followers = find_missing(new_followers, current_followers)
				add_to_list(followers, self.user['followers'])
			else:
				self.user['total-followers'] = total
				unfollowers = find_missing(current_followers, new_followers)
				remove_from_list(unfollowers, self.user['followers'])
			self.db.save(self.user)
		self.display.followers_report(followers, unfollowers)

	def report_all(self):
		'''Report both followers && followings.'''
		self.report_followings()
		self.report_followers()

	def close(self):
		'''Closes selenium application.'''
		self.client.close()

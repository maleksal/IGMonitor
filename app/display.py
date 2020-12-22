"""
Displays information to terminal
"""


class Display:
	'''Display - displays to terminal.'''
	
	def __init__(self, user):
		'''Class constructor. sets the above attributes'''
		self.profile_url = 'https://www.instagram.com/'
		self.user = user
		self.username = self.user['username']
		print('\n> Target: {}\n'.format(self.username))

	def followers_report(self, followers, unfollowers):
		'''Displays report of followers && unfollowers.'''
		print(f'recently followed by:')
		for i in followers:
			generated_link = self.profile_url + i
			print(f'\t- {i}  ({generated_link})')
		# Unfollowers
		print(f'recently unfollowed by:')
		for i in unfollowers:
			generated_link = self.profile_url + i
			print(f'\t- {i}  ({generated_link})')
		print('\n')

	def followings_report(self, followings, unfollowings):
		'''Displays report of followings && unfollowings.'''
		print('recently followed:')
		for i in followings:
			generated_link = self.profile_url + i
			print(f'\t- {i}  ({generated_link})')
		# Unfollowers
		print('recently unfollowed:')
		for i in unfollowings:
			generated_link = self.profile_url + i
			print(f'\t- {i}  ({generated_link})')
		print('\n')

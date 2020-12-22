import json
import os


class Storage:
	'''Storage acts like a database.'''
	dire = 'app/storage'

	def __init__(self, filename='test.json'):
		'''Constructor, generate file path.'''
		self.filename = self.dire + '/' + filename

	def save(self, data):
		'''Saves user in file as json.'''
		with open(self.filename, "w") as file:
			file.write(json.dumps(data, indent=True))

	def retrieve(self):
		'''Retrieves loads json from file.'''
		if os.path.exists(self.filename):
			with open(self.filename, 'r') as file:
				return json.loads(file.read())
		return None

import threading
import time
from sys import argv

from app.application import Application
from app.helpers import spinner
from decouple import config


def help():
	print('\nUsage: main.py [command] -[flag:optional] [username].')
	print('\nCommands:')
	print('\n\tregister  add new user to be monitored.')
	print('\n\tstatus	  get status of an instagram user (must supply flag)')
	print('\n\t\t -fs: report only user followers section.')
	print('\n\t\t -fg: report only user followings section.')
	print('\n\t\t -all: report both sections.\n')

	exit()

def main(target, comd, flag):
	base_url = config('BASE_URL')
	username = config('IGUSERNAME')
	password = config('PASSWORD')
	app = Application(base_url, username, password, target)

	flags = {
		'-fs': app.report_followers,
		'-fg': app.report_followings,
		'-all': app.report_all
	}
	if comd in ['status', 'register']:
		if comd == 'register':
			app.register_user()
		elif comd == 'status':
			# check flags
			if flag in flags.keys():
				flags[flag]()
			else:
				help()
	else:
		help()
	app.close()


if __name__ == '__main__':

	if len(argv) >= 3:
		# empty var flag in case of argv == 3
		flag = None
		command = argv[1]
		if len(argv) > 3:
			flag = argv[2]		
			target = argv[3]
		else:
			target = argv[2]
		thread = threading.Thread(target=main, args=(target, command, flag))
		thread.start()
		# Loading spinner
		spinner(thread)
		thread.join()
	else:
		help()

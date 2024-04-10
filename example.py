"""
	Main
"""
class App:
	app_name = 'Hello World'
	app_version = '0.0.1'

	welcome_banner = """
		welcome to %s %s
		type .help to show help or use .exit (ctrl+d) to quit shell
	"""  % (app_name, app_version)

	initial_prompt = 'Perfecto'

	commands = (
		('redcommand on', '', 'This is RED command!', 'darkred'),
		('redcommand off', '', 'This is RED command!', 'darkred'),
		('bluecommand 1', '<Argument>', 'This is BLUE command!', 'blue'),
		('bluecommand 2', '<Argument>', 'This is BLUE command!', 'blue'),
		('greencommand a', '', 'This is GREEN command!', 'green'),
		('greencommand b', '', 'This is GREEN command!', 'green'),
		('magentacommand', '[Optional Arg]', 'This is CYAN command!', 'darkmagenta'),
		('magentacommand-second', '[Optional Arg]', 'This is CYAN command!', 'darkmagenta'),
		('cyancommand', '', '', 'darkcyan'),
		('perfect', '', '', 'darkcyan'),
	)

	attributes = (
		(r'boom+'),
	)

	keywords = (
		(r'store+'),
	)


import logging
logger = logging.getLogger(__name__)

import shlex

def simple_parser(s):
	try:
		return list(shlex.shlex(s))
	except Exception:
		return s.split(' ')

from shellui.tools import (QuietResponse, TextResponse, JsonResponse, TableResponse,
				print_html, print_json, print_table, read_passphrase, read_password)


def at_begin():
	print('AT_BEGIN')

def at_end():
	print('AT_END')

def command_handler(command, spinner):

	# print logs
	logger.warning("This is message")
	logger.error("This is message")
	logger.critical("This is message")
	
	
	# start loading spinner
	spinner.start()
	
	# do something
	...
	import time
	time.sleep(1.5)
	...
	
	# stop loading spinner
	spinner.stop()

	# print other logs
	logger.debug("This is message")
	logger.info("This is message")

	# print input command and parsed command
	print(command)
	print(simple_parser(command))

	# read password and passphrase
	print(read_password(5))
	##print(read_passphrase(7))

	done = '''
	Normal Text
	<b>Bold Text</b>
	<span color="red">Red Text</span>
	<span color="cyan">Cyan Text</span>
	'''

	# Print HTML
	print_html(done)

	# Print JSON object
	print_json(dict(hello="World"))

	# Print Simple Table
	print_table([
		[1,2],
		[3,4]
	])
	
	##return TextResponse(done, html=True, prompt_text='perfect')
	##return QuietResponse()
	return JsonResponse(dict(hello=command))

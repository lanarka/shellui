'''
	Response tools
'''
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter

import json
from prettytable import PrettyTable

from prompt_toolkit import print_formatted_text as printf
from prompt_toolkit.formatted_text import HTML
from getpass import getpass

def print_html(html):
	printf(HTML(html))

def print_json(obj):
	json_str = json.dumps(obj, indent=4, sort_keys=True)
	done = highlight(json_str, JsonLexer(), TerminalFormatter())	
	print(done)

def print_table(data):
	table = PrettyTable(data[0])
	for item in data[1:]:
		table.add_row(item)
	print('\n%s\n' % table)

def read_passphrase(pass_len):
	assert pass_len >= 4
	try:
		passphrase = getpass('Choose a passphrase (min. %s characters): ' % pass_len)
	except KeyboardInterrupt:
		print()
		return read_passphrase(pass_len)
	try:
		verifypass = getpass('Re-enter passphrase: ')
	except KeyboardInterrupt:
		print()
		return read_passphrase(pass_len)
	if (passphrase != verifypass):
		print('Passphrases do not match!')
		return read_passphrase(pass_len)
	if (len(passphrase) < pass_len):
		print('Passphrase is too short!')
		return read_passphrase(pass_len)		
	return passphrase

def read_password(pass_len):
    assert pass_len >= 4
    try:
      password = getpass('Enter password: ')
    except KeyboardInterrupt:
      print()
      return read_password(pass_len)
    return password

def QuietResponse(prompt_text=''):
	return ('\n', False, '', prompt_text)

def TextResponse(text, prompt_text='', html=False):
	return ('\n', html, text, prompt_text)

def JsonResponse(obj, prompt_text=''):
	json_str = json.dumps(obj, indent=4, sort_keys=True)
	done = highlight(json_str, JsonLexer(), TerminalFormatter())
	return ('\n', False, '\n' + done, prompt_text)

def TableResponse(data, prompt_text=''):
	table = PrettyTable(data[0])
	for item in data[1:]:
		table.add_row(item)
	return ('\n\n', False, '\n'+str(table), prompt_text)

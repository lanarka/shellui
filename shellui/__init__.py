"""
	ShellUI on top of Python prompt toolkit
	---------------------------------------
	
	Usage:
	
	my_object = {
		'a': 1,
		'b': 'Hello'
	}

	my_table = (
		('Col-A', 'Col-B', 'Col-C', 'Col-D'),
		(1, 2, 3, 4),
		(5, 6, 5 ,7),
	)

	def my_command_handler(command):
		...
		from shellui.tools import TextResponse, JsonResponse, TableResponse
		return TextResponse('Hello<b>World</b>', html=True, prompt_text='Perfect')
		return TableResponse(my_table, prompt_text='Perfect')
		return JsonResponse(my_object, prompt_text='Perfect')


	if __name__ == '__main__':

		my_info = (
			('my-app',     '1.0.0'),
			('my-app-ext', '9.9.9')
		)

		my_commands = (
			#Command           Arguments                  Description               Color   
			('redCommand On',  '',                        'This is RED command!',   'darkred'),
			('redCommand Off', '',                        'This is RED command!',   'darkred'),
			('blueCommand A',  '<Argument>',              'This is BLUE command!',  'blue'),
			('blueCommand B',  '<Argument1> <Argument2>', 'This is BLUE command!',  'blue'),
			('greencommand',   '',                        'This is GREEN command!', 'green'),
		)

		from shellui import ShellUI
		my_shell = ShellUI('Hello', 
			welcome='\n\twelcome to my very cool shell\n',
			commands=my_commands,
			command_handler=my_command_handler,
			info=my_info
		)
		my_shell.loop()
"""

from prompt_toolkit.completion import Completion, Completer
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import prompt, CompleteStyle
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit import print_formatted_text as printf
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import style_from_pygments_cls
from prompt_toolkit import print_formatted_text as printf
from prompt_toolkit.formatted_text import HTML

from pygments.styles.vim import VimStyle
from pygments.lexer import RegexLexer
from pygments.token import (Number, Name, String, Text, Keyword, Operator)

from prettytable import PrettyTable
from halo import Halo
import sys
bold = lambda string: "<b>%s</b>" % string

try:
	from app.main import at_begin, at_end
except:
	def at_begin():
		pass
	def at_end():
		pass

class InputLexer(RegexLexer):
	tokens = {
		'root': [
			(r'[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)', Number),
			(r'[a-z][0-9]+', Name),
			(r'"', String, 'string'),
			(r'\s+', Text),
			(r'\.[a-z]+', Keyword),
		],
		'string': [
			(r'[^"\\]+', String),
			(r'\\.', String.Escape),
			(r'"', String, '#pop'),
		]
	}


class ShellUI:

	CMD_HELP = '.help'
	CMD_EXIT = '.exit'

	def __init__(self, name=None, command_handler=None, commands=(), info=(), 
				 welcome='', ascii_prompt=False, multiline=False, inputlexer=InputLexer):
		if ascii_prompt:
			self.prompt = '>'
		else:
			self.prompt = '\u276D'
		self.info = info
		self.commands = commands
		self.name = name
		self.welcome = welcome
		self.multiline = multiline
		self.data = self._create_data()
		self.command_handler = command_handler
		self.inputlexer = inputlexer
		at_begin()

	def _create_data(self):
		done = {}
		commands = self.commands
		_commands = []
		for c in commands:
			_commands.append(c[0])
		done['Commands'] = _commands
		_arguments = []
		for c in commands:
			_arguments.append(c[1])
		done['Arguments'] = _arguments
		_history = []
		for c in commands:
			_history.append('%s %s' % (c[0], c[1]) )
		done['History'] = _history
		_meta = {}
		for c in commands:
			_meta[c[0]] = HTML(c[2])
		done['Meta'] = _meta
		_family = {}
		for c in commands:
			_family[c[0]] = c[3]
		done['CommandsFamily'] = _family
		_family_name = {}
		for c in commands:
			tmp = c[1]
			if tmp == '':
				tmp = 'No args.'
			_family_name[c[0]] = tmp
		done['CommandsFamilyName'] = _family_name
		return done

	def _show_help(self):
		table_c = PrettyTable(['Command', 'Arguments', 'Description'])
		for item in self.commands:
			table_c.add_row([item[0], item[1], item[2]])

		table_s = PrettyTable(['Key', 'Value'])
		for item in self.info:
			table_s.add_row([item[0], item[1]])

		print()
		printf(HTML(bold('About\n')))
		print(table_s)
		print()
		printf(HTML(bold('Possible commands\n')))
		print(table_c)
		print()

	def _prepare(self, command):
		nl, fp, print_data, prompt_text = self._command_handler(command)
		if len(print_data):
			if fp:
				printf(HTML(print_data), end=nl)
			else:
				print(print_data, end=nl)
		if len(prompt_text):
			self.name = prompt_text

	def _command_handler(self, command):
		spinner = Halo(text='', spinner='dots', color='magenta')
		return self.command_handler(command, spinner)
		

	def loop(self):
		history = InMemoryHistory()
		for item in self.data['History']:
			history.append_string(item)
		session = PromptSession(
			multiline=self.multiline,
			lexer=PygmentsLexer(self.inputlexer),
			style=style_from_pygments_cls(VimStyle),
			history=history,
			auto_suggest=AutoSuggestFromHistory(),
			enable_history_search=True
		)
		data = self.data

		class ShellCompleter(Completer):
			def get_completions(self, document, complete_event):
				word = document.get_word_before_cursor()
				for cmd in data['Commands']:
					if cmd.startswith(word):
						if cmd in data['CommandsFamily']:
							family = data['CommandsFamily'][cmd]
							family_name = data['CommandsFamilyName'][cmd]
							display = HTML('<' + family + '><b>%s</b>  <i>%s</i></' + family + '>') % (cmd, family_name)
						else:
							display = cmd
						yield Completion(
								cmd,
								start_position= -len(word),
								display= display,
								display_meta= data['Meta'].get(cmd))
		if self.welcome:
			printf(HTML(bold(self.welcome)))
		while True:
			try:
				if self.name:
					prompt = HTML('<i>%s</i> <style fg="#00dd00">%s</style> ' % (self.name, self.prompt))
				else:
					prompt = HTML('<style fg="#00dd00">%s</style> ' % self.prompt)
				text = session.prompt(prompt, completer=ShellCompleter())
				cmd = text.strip()
				if cmd:
					if cmd == self.CMD_HELP:
						self._show_help()
						continue
					if cmd == self.CMD_EXIT:
						at_end()
						printf(HTML(bold('bye')))
						sys.exit(0)
					self._prepare(cmd)
			except (KeyboardInterrupt, EOFError):
				printf(HTML(bold('terminated by user')))
				sys.exit(-1)

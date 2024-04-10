"""
	Shell
"""
import argparse
import logging
import coloredlogs
import traceback
import platform
import socket
import re
import datetime

from shellui import ShellUI
from example import App, command_handler

from pygments.lexer import RegexLexer
from pygments.token import Number, Name, String, Text, Keyword, Operator

import logging
logger = logging.getLogger(__name__)

ATTRIBUTES = []
for a in App.attributes:
	ATTRIBUTES.append((a, Operator))

KEYWORDS = []
for k in App.keywords:
	KEYWORDS.append((k, Keyword))

class CommandLexer(RegexLexer):
	tokens = {
		'root': [
			(r'[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)', Number),
			(r'[a-z][0-9]+', Name),
			(r'"', String, 'string'),
			(r'\s+', Text),
			(r'\.[a-z]+', Keyword),

		] + ATTRIBUTES + KEYWORDS,
		'string': [
			(r'[^"\\]+', String),
			(r'\\.', String.Escape),
			(r'"', String, '#pop'),
		]
	}

def get_info():
	info = {}
	done = []
	info["architecture"] = platform.machine()
	if platform.processor():
		info["processor"] = platform.processor()
	info["platform"] = platform.system()
	info["platform-release"] = platform.release()
	info["platform-version"] = platform.version()
	try:
		info["hostname"] = socket.gethostname()
		info["ip-address"] = socket.gethostbyname(socket.gethostname())
		info["mac-address"] = ":".join(re.findall("..", "%012x" % uuid.getnode()))
	except:
		pass
	info["current-time"] = datetime.datetime.now().strftime("%a, %b %d %I:%M %p")
	info["python-version"] = platform.python_version()
	try:
		info["compiler-version"] = "%d.%d.%d" % (__compiled__.major, __compiled__.minor, __compiled__.micro)
	except:
		pass
	info[App.app_name]=App.app_version

	for x in info.keys():
		done.append((x, info[x]))
	return done

def on_unhandled_exception(type, value, tb):
	tbinfo = "".join(traceback.format_exception(type, value, tb))
	msg = "%s -> %s" % (type.__name__, tbinfo)
	logger.critical(msg)

def run_shell():
	sh = ShellUI(App.initial_prompt,
		welcome=App.welcome_banner,
		commands=App.commands,
		command_handler=command_handler,
		info=get_info(),
		inputlexer=CommandLexer,
	)
	sh.loop()

def start_app():
	logger = logging.getLogger(__name__)
	coloredlogs.DEFAULT_DATE_FORMAT = "%d/%m/%y %H:%M:%S"
	coloredlogs.DEFAULT_FIELD_STYLES = {
		"asctime": {"color": "green"},
		"hostname": {"color": "white", "faint": True},
		"levelname": {"color": "cyan"},
		"name": {"color": "magenta"},
		"programname": {"color": "cyan"},
		"username": {"color": "yellow"}
	}
	coloredlogs.DEFAULT_LEVEL_STYLES = {
		"critical": {"color": "red"},
		"debug": {"color": "green"},
		"error": {"color": "red"},
		"info": {"color": "white"},
		"notice": {"color": "magenta"},
		"spam": {"color": "red", "faint": True},
		"success": {"color": "green", "faint": True},
		"verbose": {"color": "blue"},
		"warning": {"color": "yellow"}
	}
	coloredlogs.install(level="DEBUG")
	run_shell()

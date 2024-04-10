"""
	Run
"""
import sys
from shell import start_app, on_unhandled_exception

if __name__ == "__main__":
	sys.excepthook = on_unhandled_exception
	sys.exit(start_app())

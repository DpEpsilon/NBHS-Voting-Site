import template
import database_engine

import argparse
from bottle import route, run, static_file, error,\
	abort, redirect, get, post, request

import os

class Page(object):
	def __init__(self, url, title):
		self.url = url
		self.title = title
pages = [
	Page('/', 'Home'),
	Page('/nominate', 'Nominate'),
	]

@route('/static/<filename:path>')
def serve_static(filename):
	return static_file(filename, root='./static')

@route('/css/<filename:re:.*\\.css>')
def serve_css(filename):
	return static_file(filename, root='./css', mimetype='text/css')

@route('/js/<filename:re:.*\\.js>')
def serve_js(filename):
	return static_file(filename, root='./js', mimetype='application/javascript')

@route('/favicon.ico')
def favicon():
	return static_file('favicon.ico', root='./', mimetype='image/x-icon')

@route('/')
def index():
	return template.render("index.html", {'pages': pages, 'page': pages[0],
										  'status': 'nominations',
										  'has_voted': True})

@get('/nominate')
def nominate_get():
	return template.render("nominate.html", {'pages': pages, 'page': pages[1]})

@post('/nominate')
def nominate_post():
	#print request.forms.get('leadership_experience')
	#print request.forms.get('why')
	return template.render("nominate.html", {'pages': pages, 'page': pages[1]})

@get('/<something:path>/')
def slash_redir_get(something):
	redirect("/" + something)

@post('/<something:path>/')
def slash_redir_post(something):
	redirect("/" + something)


if __name__ == '__main__':
	arg_parser = argparse.ArgumentParser(
		description="Runs the src voting webserver.")
	arg_parser.add_argument("-d", "--debug", action="store_const",
							const=True, default=False,
							help="Turns on traceback on 500 errors and\n"
							"sets host to 'localhost'")
	arg_parser.add_argument("-p", "--port", default="8080", nargs='?',
							help="Port for server to listen on "
							"(default: 8080).")
	args = arg_parser.parse_args().__dict__

	database_engine.init_db()
	
	if not args['port'].isdigit():
		arg_parser.print_usage()
		print "error: port must be a decimal integer"
	else:
		run(host='localhost' if args['debug'] else '0.0.0.0',
			port=args['port'], debug=args['debug'])

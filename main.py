import template
import database_engine
import cookies
import user

import json
import argparse
from bottle import route, run, static_file, error,\
	abort, redirect, get, post, request, response

import os

class Page(object):
	def __init__(self, url, title):
		self.url = url
		self.title = title
pages = [
	Page('/', 'Home'),
	Page('/nominate', 'Nominate'),
	Page('/login', 'Login')
	]

config = {}
config_vars = ["name", "status"]


def process_cookie(cookie):
	# See if they are logged in. If so display their name
	curr_user = None
	if cookie is not None:
		login_id = cookies.get_id(cookie)
		if login_id is not None:
			curr_user = user.get_user(login_id)
	return curr_user

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
	current_user = process_cookie(request.get_cookie("login"))
	return template.render("index.html", {'config': config,
										  'pages': pages, 'page': pages[0],
										  'status': 'nominations',
										  'has_voted': True,
										  'user': current_user})

@get('/nominate')
def nominate_get():
	current_user = process_cookie(request.get_cookie("login"))
	if current_user is None:
		redirect('/login?message=3')
	return template.render("nominate.html", {'config': config,
											 'pages': pages, 'page': pages[1],
											 'user': current_user})

@post('/nominate')
def nominate_post():
	#print request.forms.get('leadership_experience')
	#print request.forms.get('why')
	nominee_fields = config['nominee_fields']
	current_user = process_cookie(request.get_cookie("login"))
	return template.render("nominate.html", {'config': config,
											 'pages': pages, 'page': pages[1],
											 'user': current_user})

@get('/login')
def login_get():
	message = request.query.get('message')
	try:
		message = int(message)
	except:
		message = 0
	current_user = process_cookie(request.get_cookie("login"))
	return template.render("login.html", {'config': config,
										  'pages': pages, 'page': pages[2],
										  'valid': message,
										  'user': current_user})
@post('/login')
def login_post():
	validity = user.is_valid_login(request.forms.get('username'), request.forms.get('password'))
	current_user = process_cookie(request.get_cookie("login"))
	if validity == 0: # Success		
		cookie = cookies.give_cookie(request.forms.get('username'))
		print cookie
		response.set_cookie("login", cookie, max_age=cookies.expire_time)
		return template.render("home_redirect.html",
							   {'message': "<h1>Login Successful</h1>"})
	else:
		return template.render("login.html", {'config': config,
											  'pages': pages, 'page': pages[2],
											  'valid': validity,
											  'user': current_user})

@route('/logout')
def logout_post():
	cookie = request.get_cookie("login")
	if cookie is not None:
		cookies.remove_cookie(cookie)
	redirect("/")

@get('/<something:path>/')
def slash_redir_get(something):
	redirect("/" + something)

@post('/<something:path>/')
def slash_redir_post(something):
	redirect("/" + something)

def get_missing_config_variables():
	return list(set(config_vars).difference(set(config)))

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

	try:
		config = json.load(open("config.json"))
	except IOError:
		print "WARNING: No configuration file found."
	missing_variables = get_missing_config_variables()
	
	if len(missing_variables) > 0:
		print "WARNING: The following variables are missing "\
			"from the configuration and will default to None: " +\
			', '.join(missing_variables)
		print "There may be unexpected consequences as a result."
		for var in missing_variables:
			config[var] = None
	
	if not args['port'].isdigit():
		arg_parser.print_usage()
		print "error: port must be a decimal integer"
	else:
		run(host='localhost' if args['debug'] else '0.0.0.0',
			port=args['port'], debug=args['debug'])

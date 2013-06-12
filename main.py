import template
import database_engine
import cookies
import csrf
import user
import submissions

import json
import argparse
from bottle import route, run, static_file, error,\
	abort, redirect, get, post, request, response

import os

class Page(object):
	def __init__(self, url, title):
		self.url = url
		self.title = title

	def __eq__(self, other):
		return self.url == other.url and self.title == other.title


nomination_pages = [
	Page('/', 'Home'),
	Page('/nominate', 'Nominate'),
	Page('/login', 'Login')
	]

voting_pages = [
	Page('/', 'Home'),
	Page('/vote', 'Vote'),
	Page('/login', 'Login')
	]

pages = []

config = {}
config_vars = ["name", "status"]


def process_cookie(cookie):
	# See if they are logged in. If so display their name
	current_user = None
	if cookie is not None:
		login_id = cookies.get_id(cookie)
		if login_id is not None:
			current_user = user.get_user(login_id)
	return current_user

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

@get('/')
def index_get():
	page = Page('/', 'Home')
	current_user = process_cookie(request.get_cookie("login"))
	csrf_key = None
	if current_user is not None:
		csrf_key = csrf.get_csrf_key(current_user.userid)
	return template.render("index.html", {'config': config,
										  'pages': pages, 'page': page,
										  'csrf': csrf_key,
										  'has_voted': True,
										  'user': current_user})

@post('/')
def index_post():
	page = Page('/', 'Home')
	current_user = process_cookie(request.get_cookie("login"))
	if current_user is None:
		redirect('/')
		
	given_csrf_key = request.forms.get('csrf')
	
	if not csrf.check_csrf_key(current_user.userid, given_csrf_key):
		abort(403, "A potential CSRF attack was detected. "
			  "Please try again later.")

	field_to_delete = request.forms.get('to_delete')

	if field_to_delete is not None:
		submissions.delete_nominee_field(current_user.userid, field_to_delete)
	
	redirect('/')

@get('/vote')
def vote_get():
	page = Page('/vote', 'Vote')
	if page not in pages:
		abort(404)
	current_user = process_cookie(request.get_cookie("login"))
	#return template.render("voting.html", {'config': config,
	#									   'pages': pages, 'page': page,
	#									   'user': current_user})
	return "<h1>No.</h1>"
@get('/nominate')
def nominate_get():
	page = Page('/nominate', 'Nominate')
	if page not in pages:
		abort(404)
	current_user = process_cookie(request.get_cookie("login"))
	nominee_fields = config['nominee_fields']
	
	if current_user is None:
		redirect('/login?message=3')
		
	if current_user.student_info is None:
		return template.render("home_redirect.html",
							   {'message': "<h1>Staff cannot nominate</h1>"})
	if not current_user.student_info.is_nominee and config['prenominate']:
		return template.render("home_redirect.html",
							   {'message': "<h1>You are not a candidate.</h1>"})
	
	nominee_fields = filter(
		lambda x: x['name'] not in current_user.student_info.nominee_fields,
		nominee_fields)

	if len(nominee_fields) == 0:
		return template.render("home_redirect.html",
							   {'message': """<h1>You have already
 submitted your nomination</h1>"""})
	
	return template.render("nominate.html",
						   {'config': config,
							'nominee_fields': nominee_fields,
							'csrf': csrf.get_csrf_key(current_user.userid),
							'pages': pages, 'page': page,
							'user': current_user})

@post('/nominate')
def nominate_post():
	page = Page('/nominate', 'Nominate')
	if page not in pages:
		abort(404)
	current_user = process_cookie(request.get_cookie("login"))
	nominee_fields = config['nominee_fields']
	given_csrf_key = request.forms.get('csrf')
	
	if current_user is None:
		redirect('/login?message=3')

	if not csrf.check_csrf_key(current_user.userid, given_csrf_key):
		abort(403, "A potential CSRF attack was detected. "
			  "Please try again later.")
	
	if current_user.student_info is None:
		return template.render("home_redirect.html",
							   {'message': "<h1>Staff cannot nominate</h1>"})
	
	if not current_user.student_info.is_nominee and config['prenominate']:
		return template.render("home_redirect.html",
							   {'message': "<h1>You are not a candidate.</h1>"})
	
	nominee_fields = filter(
		lambda x: x['name'] not in current_user.student_info.nominee_fields,
		nominee_fields)

	if len(nominee_fields) == 0:
		return template.render("home_redirect.html",
							   {'message': """<h1>You have already
 submitted your nomination</h1>"""})

	truncated = False
	
	for field in nominee_fields:
		submission = request.forms.get(field['name'])
		if len(submission) > field['character_limit']:
			truncated = True
			submission = submission[:650] + "...[truncated]"
		submissions.add_nominee_field(current_user.userid,
									  field['name'], submission)

	if not config['prenominate']:
		submissions.add_nominee(current_user.userid)
	
	return template.render("home_redirect.html",
						   {'message': "<h1>Submitted" +
							" (truncated)" if truncated else "" +
							"</h1>"})

@get('/login')
def login_get():
	page = Page('/login', 'Login')
	current_user = process_cookie(request.get_cookie("login"))
	
	if current_user is not None:
		return template.render("home_redirect.html",
							   {'message': "<h1>You are already logged in</h1>"})

	message = request.query.get('message')
	try:
		message = int(message)
	except:
		message = 0
	
	return template.render("login.html", {'config': config,
										  'pages': pages, 'page': page,
										  'valid': message,
										  'user': current_user})
@post('/login')
def login_post():
	page = Page('/login', 'Login')
	current_user = process_cookie(request.get_cookie("login"))
	
	if current_user is not None:
		return template.render("home_redirect.html",
							   {'message': "<h1>You are already logged in</h1>"})
	
	validity = user.is_valid_login(request.forms.get('username'), request.forms.get('password'))
	
	if validity == 0: # Success		
		cookie = cookies.give_cookie(request.forms.get('username'))
		print cookie
		response.set_cookie("login", cookie, max_age=cookies.expire_time)
		return template.render("home_redirect.html",
							   {'message': "<h1>Login Successful</h1>"})
	else:
		return template.render("login.html", {'config': config,
											  'pages': pages, 'page': page,
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

	if config['status'] == "nominations":
		pages = nomination_pages
	elif config['status'] == "voting":
		pages = voting_pages
			
	if not args['port'].isdigit():
		arg_parser.print_usage()
		print "error: port must be a decimal integer"
	else:
		run(host='localhost' if args['debug'] else '0.0.0.0',
			port=args['port'], debug=args['debug'])

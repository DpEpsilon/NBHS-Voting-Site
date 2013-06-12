import random
import string

csrf_keys = {} # userid -> csrf key

def get_csrf_key(userid):
	key = None
	if userid not in csrf_keys:
		key = ''.join(
			[random.choice(string.ascii_letters) for x in xrange(32)])
		csrf_keys[userid] = key
	else:
		key = csrf_keys[userid]
	return key

def check_csrf_key(userid, key):
	return csrf_keys[userid] == key

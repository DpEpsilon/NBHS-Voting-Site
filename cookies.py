import random
import string

cookies = {} # Cookie -> userid

def give_cookie(userid):
    # Random 32length string of upper/lower letters
    new_cookie = ''.join([random.choice(string.ascii_letters) for x in xrange(32)])
    while new_cookie in cookies:
        new_cookie = ''.join([random.choice(string.ascii_letters) for x in xrange(32)])
    cookies[new_cookie] = userid
    return new_cookie

def get_id(cookie):
    if cookie not in cookies:
        return None
    return cookies[cookie]

def remove_cookie(cookie):
    if cookie in cookies:
        del cookies[cookie]
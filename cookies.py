from collections import deque
import time
import random
import string

expire_time = 60*60*12 # 12 hours

cookies = {} # Cookie -> userid
toRemove = deque([]) # (Cookie, create_time)

def expire_cookies():
    while len(toRemove) and toRemove[0][1] + expire_time < time.time():
        remove = toRemove.popleft()
        if remove in cookies:
            del cookies[remove[0]]

def give_cookie(userid):
    expire_cookies()
    # Random 32length string of upper/lower letters
    new_cookie = ''.join([random.choice(string.ascii_letters) for x in xrange(32)])
    while new_cookie in cookies:
        new_cookie = ''.join([random.choice(string.ascii_letters) for x in xrange(32)])
    cookies[new_cookie] = userid
    toRemove.append((new_cookie, time.time()))
    return new_cookie

def get_id(cookie):
    expire_cookies()
    if cookie not in cookies:
        return None
    return cookies[cookie]

def remove_cookie(cookie):
    if cookie in cookies:
        del cookies[cookie]
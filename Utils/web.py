from re import sub
from flask import request
import functools

#decorators
def requireMethod(method:str):
	def wrap(func):
		func.__dict__['method'] = method.upper()
		@functools.wraps(func)
		def wrapped(*args,**kwargs):
			if wrapped.__dict__['method'] == 'ANY': return func(*args,**kwargs)
			if request.method == func.__dict__['method']:
				return func(*args,**kwargs)
			else: return {'failed': True, 'status': 400, 'message': 'unsupported request method for endpoint'}
		return wrapped
	return wrap

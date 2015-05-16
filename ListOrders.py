import math

def orders(l,func,args=()):
	"""Runs func(b,*args), where b is one order of list l, for every order.
	if func(b,*args) returns True, the loop is stopped
	Note: len(args) must be != 1 (don't know, why...)
	"""
	if len(args) == 1:
		raise AttributeError,"len(args) must be != 1 (0,2,3,4,5,etc. are ok.)"
	def x(b,o,args): #b=liste der besetzten Zahlen o=liste der offenen Zahlen
		if len(o) >= 1:
			for i in o:
				o2=o[:]
				o2.remove(i)	#i von o nehmen
				if x(b+[i],o2,args):	#und i zu b tun
					return True
		else:
			if func(b,*args):
				return True
	x([],l,args)

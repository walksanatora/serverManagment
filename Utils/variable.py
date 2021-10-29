

def removeNone(di:dict) -> dict:
	"""Removes all NoneTypes from a given dict recursively"""
	out = {}
	for k in di.keys():
		if not di[k] == None:
			if type(di[k]) == type({}):
				out[k] = removeNone(di[k])
			else: out[k] = di[k]
	return out

def dictConvertString(di:dict,sep:str) -> list:
	"""Convert a dictionary to a list of strings joined by `sep`"""
	lis = []
	for k in di.keys():
		if type(di[k]) == type({}):
			for i in dictConvertString(di[k],sep):
				lis.append(f'{k}{sep}{i}')
		else:
			lis.append(di[k].name)
	return lis

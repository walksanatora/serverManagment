import inspect


class abstractFunction:
	name: str
	args: list
	_d_: dict
	def __init__(self,name:str,args:list,**kwargs):
		self.__dict__ = kwargs
		self.name = name
		self.args = args
	def __str__(self) -> str:
		return f'{self.name}({",".join(self.args)})'
	def __repr__(self) -> str:
		return self.__str__()
	

def dump(val,**kwargs) -> dict:
	if inspect.isfunction(val):
		hasKwarg = False
		Params = inspect.signature(val).parameters
		args = []
		for arg in list(Params)[1:]:
			targ = Params[arg]
			if targ.kind == targ.VAR_KEYWORD:
				hasKwarg = True
			else:
				args.append(arg)
		if hasKwarg:
			return abstractFunction(val.__name__,args,**val.__dict__)
	if inspect.isclass(val):
		d = dir(val)
		out = {}
		for i in d:
			if not i.startswith('_'):
				out[i] = dump(getattr(val,i))
		return out

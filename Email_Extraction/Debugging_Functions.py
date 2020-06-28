def Return_Instance(Obj):
	if isinstance(Obj, str):
		return "String"
	elif isinstance(Obj, list):
		return "List"
	else:
		return "Unknown Type"
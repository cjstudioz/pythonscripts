import importlib.util
import os
import glob
import yaml
from collections.abc import Mapping  # like dict


def update_nested(origdict: dict, updatedict: dict):
	"""
	NOTE: doesn't preserve order of list and tuples

	"""
	for updatekey, updateval in updatedict.items():
		origval = origdict.get(updatekey, {})
		if all([  # if both updateval, origval are dicts then recurse
			isinstance(x, Mapping) for x in [updateval, origval]
		]):
			origdict[updatekey] = update_nested(origval, updateval)
		elif all([  # if both updateval, origval are list like
			isinstance(x, (set, tuple, list)) for x in [updateval, origval]
		]):
			origdict[updatekey] = list(set(updateval).union(set(origval)))
		else:
			origdict[updatekey] = updateval

	return origdict

def load_module(path):
    module_name = path.replace(os.path.sep, '.').replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

#inputs
def generate_config(
	lambda_root = r'lambdas'
):
	paths = glob.glob(lambda_root + '/**/*.py', recursive=True)
	modules = [load_module(path) for path in paths if '__init__' not in path]

	result = {}
	for module in modules:
		for property in dir(module):
			name_prefix = module.__name__.replace('.', '-').replace(lambda_root, '')[1:]

			if property.startswith(('put__', 'get__', 'post__')):
				handler = f'{module.__name__}.{property}'
				method, suffix = property.split('__')
				name = '-'.join(filter(None, [name_prefix, method, suffix]))

				obj = getattr(module, property)
				overrides = getattr(obj, 'serverless_overrides', {})

				derived_config = {
					'handler': handler,
					'layers': '',
					'events': [
						{
							'http': {
								'path': name.replace('-', '/'),
								'method': method.upper(),
								'cors': True
							},
						},
					],
				}
				result[name] = update_nested(derived_config, overrides)
	return result

def generate_yml(*args, **kwargs):
	result = generate_config(*args, **kwargs)
	yamlstr = yaml.safe_dump(result)
	return yamlstr

if __name__ == '__main__':
	res = generate_yml()
	print(res)
	with open('serverless.yml', 'w') as file:
		file.write(res)

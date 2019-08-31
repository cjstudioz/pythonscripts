import importlib.util
import os
import glob
import yaml

#inputs
lambda_root = r'lambdas'


def load_module(path):
    module_name = path.replace(os.path.sep, '.').replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

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

			result[name] = {
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

yamlstr = yaml.safe_dump(result)
print(yamlstr)

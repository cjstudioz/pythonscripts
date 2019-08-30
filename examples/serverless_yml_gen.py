import importlib.util
import os
import glob
import yaml

#inputs
lambda_root = r'lambdas'


def load_module(path):
    module_name = file.replace(os.path.sep, '.').replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

paths = glob.glob(lambda_root + '/**/*.py', recursive=True)
modules = [load_module(path) for path in paths if '__init__' not in path]

result = {}
for module in modules:
    path = module.__name__
    name = path.replace('.', '-').replace(lambda_root, '')[1:]
    url = name.replace('-', '/')
    overrides = module.AWS_LAMBDA_CFG
    

result = {
	'functions': {
		file: {
		    'handler': file,
		    'layers': '',
		    'events': [
			    {
				    'http': {
						'path': file.replace('.', '/'),
						'method': 'GET',
					    'cors': True
				    },
			    },
			],
		}
	}
}
yamlstr = yaml.safe_dump(result)
print(yamlstr)

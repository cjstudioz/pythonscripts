
import os
import glob
import yaml

my_path = r'lambdas' #r'lambdas'
files = glob.glob(my_path + '/**/*.py', recursive=True)
handlers = [file.replace(os.path.sep, '.').replace('.py', '.default') for file in files if '__init__' not in file]



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
	for file in handlers}
}
yamlstr = yaml.safe_dump(result)
print(yamlstr)



env-export:
	conda env export | grep -v '^prefix: ' > environment.yml
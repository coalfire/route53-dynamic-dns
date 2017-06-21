test:
	nosetests --verbose --rednose

venv:
	@virtualenv -p $$(which python3) venv
	@echo "Now run this"
	@echo '    . venv/bin/activate'
	@echo 'To stop using virtualenv, run this'
	@echo '    deactivate'

requirements:
	@pip install -r requirements.txt

freeze: freeze_requirements

freeze_requirements:
	@pip freeze > requirements.txt
	@git add requirements.txt
	@git commit -m 'freeze requirements' requirements.txt


play: play.py
	python3 play.py


install: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt
	


install: 
	pip3 install --upgrade pip && pip3 install -r requirements.txt

format: 
	black *.py



all: install format 

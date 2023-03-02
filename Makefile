run-server:
	python3 server.py
run-client:
	python3 client.py
	
	

install:
	pip install -r requirements.txt

build:
	python setup.py build bdist_wheel

clean:
	if exist "./build" rd /s /q build
	if exist "./dist"  rd /s /q dist
	if exist "./myprojectname.egg-info" rd /s /q myprojectname.egg-info

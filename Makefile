deploy:
	appcfg.py -A third-party-return update .

run:
	dev_appserver.py .

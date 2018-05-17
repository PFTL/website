run:
	pelican -t theme -s settings.py -o output/ content
	cp -r static/* output/static/



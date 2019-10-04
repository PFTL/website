run:
	pelican -t theme -s settings.py -o output/ content
	cp -r static/* output/static/

publish:
	pelican -t theme -s settings_publish.py -o output/ content
	cp -r static/* output/static/

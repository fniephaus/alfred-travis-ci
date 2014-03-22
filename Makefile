all:
	cd src ; \
	zip ../Travis-CI-for-Alfred.alfredworkflow . -r --exclude=*.DS_Store*

clean:
	rm -f *.alfredworkflow
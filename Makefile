init:
	python setup.py develop
test: init
	curl http://rkt-elasticsearch:9200/_all -X DELETE
	curatorMigrations \
		--elasticsearch-host=rkt-elasticsearch\
		--action-files-path=./samples/actions/\
		--force-index-creation=false\
		--dry-run=false\
		--config-file=samples/curator.yml\
		--override-running-state=true

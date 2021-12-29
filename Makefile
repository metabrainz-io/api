DIR := $(CURDIR)

default: build up
destroy: kill remove

build:
	docker build -t metabrains/api_test -f Dockerfile .
up:
	docker run -d -p 8000:8000 -v $(DIR):/api --name mb_api metabrains/api_test
dev:
	docker run -it --rm -p 8000:8000 -v $(DIR):/api --name mb_api metabrains/api_test bash
kill:
	docker container kill mb_api
remove:
	docker container rm mb_api
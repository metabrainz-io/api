DIR := $(CURDIR)

default: build up
destroy: kill remove

build:
	docker build -t metabrains/mb_api_dev -f Dockerfile .
up:
	docker run -d -p 5000:5000 -v $(DIR):/api --name mb_api metabrains/mb_api_dev
dev:
	docker run -it --rm -p 5000:5000 -v $(DIR):/api --name mb_api metabrains/mb_api_dev bash
kill:
	docker container kill mb_api
remove:
	docker container rm mb_api

DIR := $(CURDIR)

default: build up

build:
	docker build -t doselabs/api_test -f Dockerfile .

up:
	docker run -d -p 8000:8000 -v $(DIR):/api --name dlapi_test doselabs/api_test

attach:
	docker exec -it api bash

down: kill remove

kill:
	docker container kill api

remove:
	docker container rm api

dev:
	docker run -it --rm -p 8000:8000 -v $(DIR):/api --name dlapi_test doselabs/api_test bash
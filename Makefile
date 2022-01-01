DIR := ${CURDIR}

build:
	docker build -t metabrainz/mb_api_base -f Dockerfile .
test:
	docker run -d --mount type=bind,source=$(DIR)/api,target=/api -p 5000:5000 --name mb_api_base metabrainz/mb_api_base
publish:
	docker tag metabrainz/mb_api_base bwo0877hpnza/mb_api_base:0.1
	docker push bwo0877hpnza/mb_api_base:0.1

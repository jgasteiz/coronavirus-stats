#!make
include .env
export

serve:
	flask run --host=0.0.0.0

lint:
	isort -rc .
	black .

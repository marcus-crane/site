develop:
	docker-compose up --build

deploy:
	docker-compose -f production.yml up --build -d

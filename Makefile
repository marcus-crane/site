dev:
	docker-compose up --build

deploy:
	docker-compose down
	git pull origin master
	docker-compose -f production.yml up --build -d
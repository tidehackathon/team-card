build-docker:
	docker build -t api_image .


run-docker:
	docker run --name api_container -p 80:80 --rm api_image


API_CONTAINER_ID=`docker ps --filter "ancestor=api_image" --format "{{.ID}}"`
stop-docker:
	docker stop ${API_CONTAINER_ID} 


exec-docker:
	docker exec -it ${API_CONTAINER_ID} bash


stop-docker:
	docker stop api_container

setup-local-api:
	uvicorn api:app --reload
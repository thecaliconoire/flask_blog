start:
	docker build --tag techtrends ./techtrends
	docker run -d -p 7111:3111 techtrends:latest
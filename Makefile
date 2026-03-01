IMAGE  = governance-analysis-engine
PORT   = 5577

.PHONY: build run up stop

build:
	docker build -t $(IMAGE) .

run:
	docker run -p $(PORT):$(PORT) $(IMAGE)

up: build run

stop:
	docker stop $$(docker ps -q --filter ancestor=$(IMAGE))

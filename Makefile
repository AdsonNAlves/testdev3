APP_NAME=raspi-vision-api
IMAGE_NAME=$(APP_NAME):latest
CONTAINER_NAME=$(APP_NAME)_container

# ------- HELP -------
help:
	@echo ""
	@echo "Comandos disponíveis no Makefile:"
	@echo ""
	@echo "  make help        - Mostrar esta ajuda"
	@echo "  make build       - Construir a imagem do container"
	@echo "  make run         - Iniciar a aplicação em modo container"
	@echo "  make stop        - Parar e remover o container"
	@echo "  make logs        - Mostrar logs em tempo real"
	@echo "  make restart     - Reiniciar o container"
	@echo "  make shell       - Entrar no shell do container"
	@echo "  make push        - Enviar imagem para o Docker Hub/Registry"
	@echo ""

# ------- BUILD -------
build:
	podman build -t $(IMAGE_NAME) .

# ------- RUN -------
run:
	podman run -d --name $(CONTAINER_NAME) -p 8000:8000 $(IMAGE_NAME)

# ------- STOP -------
stop:
	-podman stop $(CONTAINER_NAME)
	-podman rm $(CONTAINER_NAME)

# ------- LOGS -------
logs:
	podman logs -f $(CONTAINER_NAME)

# ------- RESTART -------
restart: stop run

# ------- SHELL -------
shell:
	podman exec -it $(CONTAINER_NAME) /bin/bash

# ------- PUSH -------
push:
	podman push $

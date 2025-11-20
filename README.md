# Raspberry Pi Vision API (FastAPI + YOLOv8 + Podman)

Este projeto fornece uma API FastAPI embarcada na Raspberry Pi, capaz
de:

-   Detectar objetos em imagens
-   Contar pessoas
-   Gerar previsões simples em tempo real
-   Expor endpoints REST acessíveis via rede local
-   Rodar totalmente em um container Podman

## 🚀 Requisitos

-   Raspberry Pi 4 (4GB ou 8GB)

-   Raspberry Pi OS 64 bits ou Ubuntu ARM64

-   Podman instalado:

    ``` bash
    sudo apt install podman -y
    ```

## 📦 Estrutura do Projeto

    .
    ├── app/
    │   ├── main.py
    ├── Dockerfile
    ├── requirements.txt
    ├── Makefile
    └── README.md

## 🛠️ Construir o container

    make build

## ▶️ Rodar o container

    make run

A API ficará acessível em:

    http://RASPBERRY_IP:8000/docs

## 🛑 Parar o container

    make stop

## 🔍 Ver logs

    make logs

## 🔥 Endpoints

### Healthcheck

    GET /health

### Detectar objetos

    POST /detect/image

### Contar pessoas

    POST /detect/people

### Previsão simples

    GET /predict/live

## 📷 Upload de imagens

Via curl:

    curl -X POST -F "file=@imagem.jpg" http://testvison:8000/detect/image

## 📄 Licença

MIT
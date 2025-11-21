# Raspberry Pi Vision API (FastAPI + YOLOv8 + Podman)

Este projeto fornece uma API FastAPI embarcada na Raspberry Pi, capaz
de:

-   Detectar objetos em imagens\
-   Rodar container Podman automático ao ligar a rasp\
-   Makefile

## 🚀 Requisitos

-   Raspberry Pi 4 (4GB ou 8GB)\
-   Raspberry Pi OS 64 bits ou Ubuntu ARM64\
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

# Inicialização Container

``` bash
podman run -d --name raspi-vision-api_container -p 8000:8000 localhost/raspi-vision-api:latest
```

## Arquivo Systemd

``` bash
podman generate systemd --name raspi-vision-api_container --new --files
```

``` bash
mkdir -p ~/.config/systemd/user
mv container-raspi-vision-api_container.service ~/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user enable container-raspi-vision-api_container.service
systemctl --user start container-raspi-vision-api_container.service
```

## "lingering" 

``` bash
sudo loginctl enable-linger $USER
```
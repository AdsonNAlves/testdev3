from fastapi import FastAPI
from ultralytics import YOLO
from PIL import Image
import requests
import io
import time
import cv2
import numpy as np
from fastapi.responses import StreamingResponse

app = FastAPI()

# Carrega o modelo pré-treinado padrão da Ultralytics
model = YOLO("yolov8n.pt")


@app.get("/detect/imgjson")
async def detect_image_json(url: str, confidence: float = 0.8):
    # Download da imagem
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert("RGB")

    start_time = time.time()

    # Inferência
    results = model(image, conf=confidence)  
    result = results[0]

    detections = []
    class_counts = {}

    for i, box in enumerate(result.boxes):
        cls_id = int(box.cls)
        cls_name = model.names[cls_id]
        conf = float(box.conf)

        # Contagem
        class_counts[cls_name] = class_counts.get(cls_name, 0) + 1

        # Lista de detecções
        detections.append({
            "id": i,
            "class_id": cls_id,
            "class_name": cls_name,
            "confidence": conf,
            "bbox": {
                "xmin": float(box.xyxy[0][0]),
                "ymin": float(box.xyxy[0][1]),
                "xmax": float(box.xyxy[0][2]),
                "ymax": float(box.xyxy[0][3]),
            }
        })

    infer_time = int((time.time() - start_time) * 1000)

    return {
        "image_url": url,
        "detections": detections,
        "metadata": {
            "model": "yolov8n.pt",
            "classes_model": model.names,
            "classes_detect": list(set([d["class_name"] for d in detections])),
            "bbox_format": "xyxy",
        },
        "confidence_min": confidence,
        "quant_detect": class_counts,
        "inference_time_ms": infer_time
    }


@app.get("/detect/imgpng")
async def detect_imgpng(url: str, confidence: float = 0.8):
    # Download da imagem
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    image = Image.open(io.BytesIO(response.content)).convert("RGB")

    # Inferência e anotação
    results = model(image, conf=confidence)
    plotted = results[0].plot()  # numpy BGR

    # Converter para PNG
    img_pil = Image.fromarray(cv2.cvtColor(plotted, cv2.COLOR_BGR2RGB))
    img_bytes = io.BytesIO()
    img_pil.save(img_bytes, format="PNG")
    img_bytes.seek(0)

    return StreamingResponse(img_bytes, media_type="image/png")

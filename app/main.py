from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import cv2
import numpy as np

app = FastAPI(title="Raspberry Pi Vision API")

model = YOLO("yolov8n.pt")

def count_people(results):
    count = 0
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                count += 1
    return count

@app.get("/health")
def health_check():
    return {"status": "ok", "device": "Raspberry Pi 4"}

@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    results = model(img, verbose=False)
    boxes = results[0].boxes

    detections = [{
        "class": model.names[int(box.cls[0])],
        "confidence": float(box.conf[0]),
        "bbox": box.xyxy[0].tolist()
    } for box in boxes]

    return JSONResponse(content={
        "objects_detected": len(detections),
        "detections": detections
    })

@app.post("/detect/people")
async def detect_people(file: UploadFile = File(...)):
    contents = await file.read()
    img_array = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    results = model(img, verbose=False)
    total_people = count_people(results)

    return {"people_count": total_people}

@app.get("/predict/live")
def live_prediction():
    import random
    value = random.randint(0, 10)
    prediction = value + random.uniform(-1, 1)
    return {"current": value, "predicted_5s": prediction}

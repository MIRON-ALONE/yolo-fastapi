from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from ultralytics import YOLO, settings, solutions
import cv2

app = FastAPI()
settings.update({"datasets_dir": "/app/datasets/coco/images/train2017"})
model = YOLO(model="yolo11n.pt")
#model = YOLO("runs/detect/train/weights/best.pt")
if __name__ == "__main__":
    results = model.train(data="/app/datasets/coco/images/train2017", epochs=100, imgsz=640)
print("training were successful")
url = os.getenv("REQUEST_URL")

cropper = solutions.ObjectCropper(
    model="yolo11n.pt", 
    classes=[1, 2],  
    crop_dir="uploads",  # Папка для сохраненных объектов
)


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)



@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "url": f"/files/{file.filename}"}


@app.post("/upload-and-analize/")
async def upload_and_analize(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:      
        shutil.copyfileobj(file.file, buffer)
    image = cv2.imread(file_location)
    #print(f"{image}")
    results = model.predict(image, save=True, conf=0.01)
    result =  results[0].plot
    print(f"this is result: {result}") 
    print(f"Type of results: {type(result)}") 
    results = cropper(image)
    print(f"Results: {results}")

 # Возвращаем ссылку на итоговое изображение
    return {"filename": file.filename, "url": "app/uploads"}

@app.get("/files/")
async def list_files():
    """Возвращает список файлов в папке uploads."""
    try:
        files = os.listdir(UPLOAD_DIR)  # Получаем список файлов
        return {"files": files}
    except FileNotFoundError:
        return {"error": "Папка не найдена"}
   


app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")
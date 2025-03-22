from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from ultralytics import YOLO
import cv2

app = FastAPI()
model = YOLO(model="yolo11n.yaml")
url = os.getenv("REQUEST_URL")



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
    #print("image os.imread successfully")
    results = model(image)
    print(f"this is result: {results}") 
    print(f"Type of results: {type(results)}") 
    result_path = os.path.join(results.save_dir, results.path)
    print(f"result_path: {result_path}")
    with open(result_path, "rb") as f:
     return Response(f.read(), media_type="image/jpeg")
    #return FileResponse(path=result_path)
    #result_file =  os.path.join(UPLOAD_DIR, results)
    #cv2.imwrite(result_file, results)
    #print("image saved")
    #return {"filename": file.filename, "url": f"/files/{file.filename}"}



app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")
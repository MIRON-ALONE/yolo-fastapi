from fastapi import FastAPI, UploadFile, File
import os
import cv2

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    file_location = f"uploads/{file.filename}"
    os.write
    with open(file_location, "wb") as f:
        f.write(await file.read())  
    
    image = cv2.imread(f"{file_location}", cv2.IMREAD_COLOR)
    if image is not None:
        print("Изображение успешно загружено!")
    else:
        print("Не удалось загрузить изображение.")
   # return {"info": f"File saved at {file_location}"}


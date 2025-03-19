from fastapi import FastAPI, UploadFile, File
import os
import cv2

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    file_location = f"/uploads/{file.filename}"
    url = os.getenv("REQUEST_URL")
    image_url = f"{url}{file_location}"
    print(image_url)
    img = cv2.imread(image_url, cv2.IMREAD_COLOR)
    cv2.imwrite( image_url, img )
    return {"info": f"Image uploaded successfully at {image_url}"}

    #file_location = f"uploads/{file.filename}"
    #os.write
    #f.write(await file.read())  
   # return {"info": f"File saved at {file_location}"}


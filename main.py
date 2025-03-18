from fastapi import FastAPI, UploadFile, File
import os

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    upload_dir = "uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    file_location = f"uploads/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())  
    return {"info": f"File saved at {file_location}"}


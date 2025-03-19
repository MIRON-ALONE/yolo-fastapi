from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
import shutil
import os

app = FastAPI()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Endpoint to upload files
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename, "url": f"/files/{file.filename}"}

# Serve uploaded files
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")


# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     upload_dir = "uploads"
#     if not os.path.exists(upload_dir):
#         os.makedirs(upload_dir)
    
#     file_location = f"/uploads/{file.filename}"
#     url = os.getenv("REQUEST_URL")
#     image_url = f"{url}{file_location}"
#     print(image_url)
#     img = cv2.imread(image_url, cv2.IMREAD_COLOR)
#     cv2.imwrite( image_url, file )
#     return {"info": f"Image uploaded successfully at {image_url}"}

#     #file_location = f"uploads/{file.filename}"
#     #os.write
#     #f.write(await file.read())  
#    # return {"info": f"File saved at {file_location}"}


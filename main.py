from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, Response, JSONResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from ultralytics import YOLO, settings
import cv2

app = FastAPI()
settings.update({"datasets_dir": "/app/datasets/coco/images/train2017"})
model = YOLO(model="yolo11n.pt")
#model = YOLO("runs/detect/train/weights/best.pt")
if __name__ == "__main__":
    results = model.train(data="/app/datasets/coco/images/train2017", epochs=100, imgsz=640)
print("training were successful")
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
    results = model.predict(image, save=True, conf=0.01)
    result =  results[0].plot
    print(f"this is result: {result}") 
    print(f"Type of results: {type(result)}") 
# Access the results
    for result in results:
        xywh = result.boxes.xywh  # center-x, center-y, width, height
        xywhn = result.boxes.xywhn  # normalized
        xyxy = result.boxes.xyxy  # top-left-x, top-left-y, bottom-right-x, bottom-right-y
        xyxyn = result.boxes.xyxyn  # normalized
        names = [result.names[cls.item()] for cls in result.boxes.cls.int()]  # class name of each box
        confs = result.boxes.conf 

        print(f"---confs---: {confs}") # confidence score of each box

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy.int().tolist()
            class_name = result.names[int(box.cls)]
            confidence = box.conf
            label = f"{class_name} {confidence:.2f}"

            cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Сохраняем итоговое изображение
    output_path = os.path.join(UPLOAD_DIR, "output.jpg")
    cv2.imwrite(output_path, image)
    print("Image saved successfully")

    # Возвращаем ссылку на итоговое изображение
    return {"filename": file.filename, "url": f"/files/output.jpg"}

    #print(f"---save dir---: {result.save_dir}")
    #print(f"---results path---: {result.results_path}")
    #result_path = os.path.join(results.save_dir, results.path)
    #print(f"result_path: {result_path}")
    #with open(result_path, "rb") as f:
    # return Response(f.read(), media_type="image/jpeg")
    #return FileResponse(path=result_path)
    #result_file =  os.path.join(UPLOAD_DIR, results)
    #cv2.imwrite(result_file, results)
    #print("image saved")
    #return {"filename": file.filename, "url": f"/files/{file.filename}"}

app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")
# yolo-fastapi

данное приложение можно протестировать, запустив в сваггере. 

Dockerfile, process_voc_data, coco.yaml и docker compose собирают приложение

@app.post("/upload/") - тест для загрузки файла
@app.post("/upload-and-analize/") - анализ и обрезка изображения при помощи yolo - загружает в папку итоговые изображения
@app.get("/files/") - получает список файлов в виде ссылок, вот пример:
{
  "files": [
    "https://yolo-fastapi-production.up.railway.app/files/crop_4.jpg",
    "https://yolo-fastapi-production.up.railway.app/files/crop_8.jpg",
    "https://yolo-fastapi-production.up.railway.app/files/crop_3.jpg",
    ...

main.py --> 

cropper = solutions.ObjectCropper(
    model="yolo11n.pt", 
    classes=[1, 2],     <------ можно указать нужные классы для поиска на изображении
    crop_dir="uploads",  
)



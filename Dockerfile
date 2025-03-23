# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы, включая OpenGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx ffmpeg libsm6 libxext6 wget unzip

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . .

RUN mkdir -p /app/datasets

RUN wget -q --no-check-certificate -O /app/datasets/VOCtrainval_06-Nov-2007.zip https://github.com/ultralytics/assets/releases/download/v0.0.0/VOCtrainval_06-Nov-2007.zip \
    && unzip /app/datasets/VOCtrainval_06-Nov-2007.zip -d /app/datasets/ \
    && rm /app/datasets/VOCtrainval_06-Nov-2007.zip

#RUN wget -q --no-check-certificate -O /app/datasets/VOCtest_06-Nov-2007.zip https://github.com/ultralytics/assets/releases/download/v0.0.0/VOCtest_06-Nov-2007.zip \
#    && unzip /app/datasets/VOCtest_06-Nov-2007.zip -d /app/datasets/ \
#    && rm /app/datasets/VOCtest_06-Nov-2007.zip  
    
#RUN wget -q --no-check-certificate -O /app/datasets/VOCtrainval_11-May-2012.zip https://github.com/ultralytics/assets/releases/download/v0.0.0/VOCtrainval_11-May-2012.zip \
#&& unzip /app/datasets/VOCtrainval_11-May-2012.zip -d /app/datasets/ \
#&& rm /app/datasets/VOCtrainval_11-May-2012.zip

# Запуск обработки данных (конвертация аннотаций в YOLO формат)
RUN python /app/scripts/process_voc_data.py

# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]


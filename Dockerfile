# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем зависимости системы, включая OpenGL
RUN apt-get update && apt-get install -y libgl1-mesa-glx ffmpeg libsm6 libxext6

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы проекта
COPY . .

RUN mkdir -p /app/datasets


#RUN wget --no-check-certificate -O /app/datasets/coco128.zip https://github.com/ultralytics/assets/releases/download/v0.0.0/coco128.zip \
#    && unzip /app/datasets/coco128.zip -d /app/datasets/ \
#    && rm /app/datasets/coco128.zip


# Открываем порт 8000
EXPOSE 8000

# Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

